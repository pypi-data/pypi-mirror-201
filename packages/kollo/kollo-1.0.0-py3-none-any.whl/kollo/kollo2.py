import re
from collections import defaultdict, Counter

import os
from tqdm import tqdm

import math
from functools import reduce

_log2 = lambda x: math.log2(x)

_product = lambda s: reduce(lambda x, y: x * y, s)

_SMALL = 1e-20


def _is_match(query, target, case_sensitive, stopwords):
    """
    Does query match target? can be regex, stopwords might exist, etc
    """
    if not query:
        return True
    if stopwords and target in stopwords:
        return False
    if isinstance(query, str):
        if case_sensitive:
            return query in target
        else:
            return query.lower() in target.lower()
    return re.search(query, target)


def from_words(words, query, target, output, case_sensitive, stopwords):
    """
    Turn located matches into a frequency dictionary
    """
    ngram_freq = defaultdict(int)

    pbar = tqdm(ncols=120, unit="match", desc="Formatting collocates", total=len(words))

    for match in words:
        pbar.update()
        already_matched = False
        for pieces in match:
            targ = pieces[target].strip()
            outp = "/".join(pieces[x] for x in output)
            if not case_sensitive:
                outp = outp.lower()
            if _is_match(query, targ, case_sensitive, stopwords):
                already_matched = True
                for pieces_again in match:
                    tok = pieces_again[target].strip()
                    outp_again = "/".join(pieces_again[x] for x in output)
                    if not case_sensitive:
                        outp_again = outp_again.lower()
                    if tok is None or tok == targ:
                        continue
                    if stopwords and (pieces_again[0] in stopwords or pieces_again[-1] in stopwords):
                        continue
                    ngram_freq[(outp, outp_again)] += 1

    pbar.close()

    return ngram_freq



def _get_start_and_end(match, left, right, span, boundaries, total_lines, offsets):
    """
    Find the left and right edges for a given matching query
    """
    span_length = None
    if right is not None and right != -1:
        likely_end = min(total_lines, match + right)
    else:
        likely_end = total_lines
    if left is not None and left != -1:
        likely_start = max(0, match - left)
    else:
        likely_start = 0
    if not span:
        to_sub = sum([bool(q) for q in boundaries[likely_start:match]])
        likely_start = max(0, likely_start - to_sub)
        to_add = sum([bool(q) for q in boundaries[match:likely_end]])
        likely_end = min(total_lines, likely_end + to_add)
        return offsets[likely_start], likely_start, likely_end, span_length
    # toto: here i could put the span plus lr part?

    before = reversed(boundaries[:match])
    best_start = next((match-i for i, tag in enumerate(before) if tag == span), 0)
    best_end = next((match+i for i, tag in enumerate(boundaries[match:]) if tag == span), total_lines)
    return offsets[best_start], best_start, best_end, best_end - best_start


def _fix_output(output):
    if not isinstance(output, (tuple, list)):
        if isinstance(output, str):
            return [int(x.strip()) for x in output.split(",")]
        else:
            return [output]
    else:
        return [int(x) for x in output]
    return output

def _get_window_size(left, right, window_size):
    """
    Try to get the best possible divisor for the ngram score
    """
    if  window_size is not None:
        return max(1.0, window_size)
    if left == -1 or not left:
        window_size = right - 1.0
    elif right == -1 or not right:
        window_size = left - 1.0
    elif left and right:
        window_size = ((left + right) / 2.0 ) - 1.0
    if window_size:
        return max(1.0, window_size)
    return 1.0

def _prepare_query(query, case_sensitive):
    """
    Any preprocessing needed for our query? i.e. compiling
    """
    if query and isinstance(query, str) and not query.isalnum():
        if case_sensitive:
            flags = {}
        else:
            flags = {"flags": re.IGNORECASE}
        return re.compile(query, **flags)
    elif query:
        return str(query)


def _log_dice(ngram_freq, both_tokens, total_words):
    (w1, w2) = both_tokens
    return 2 * ngram_freq / (w1 + w2)


def _mi3(ngram_freq, both_tokens, total_words):
    power = 3
    return ngram_freq**power / _product(both_tokens)


def _mi(ngram_freq, both_tokens, total_words):
    ngram_size = 2
    return _log2(ngram_freq * total_words ** (ngram_size - 1)) - _log2(_product(both_tokens))


def _tscore(ngram_freq, both_tokens, total_words):
    expected = (both_tokens[0] * both_tokens[1]) / total_words
    t_score = math.log2((ngram_freq - expected) / math.sqrt(expected))
    return t_score


def _zscore_old(ngram_freq, both_tokens, total_words):
    expected = (both_tokens[0] * both_tokens[1]) / total_words
    np = ngram_freq * expected
    exp_less = 1 - expected
    return (ngram_freq - np) / math.sqrt(n * p * (exp_less))


def _zscore(ngram_freq, both_tokens, total_words):
    expected = (both_tokens[0] * both_tokens[1]) / total_words
    summed = total_words - expected
    std_dev = math.sqrt((summed * summed) / total_words)
    return (ngram_freq - expected) / std_dev

def _likelihood_ratio(ngram_freq, both_tokens, total_words):
    (w1, w2) = both_tokens
    n_oi = w2 - ngram_freq
    n_io = w1 - ngram_freq
    cont = (ngram_freq, n_oi, n_io, total_words - ngram_freq - n_oi - n_io)
    comb = sum(cont)
    pieces = []
    for i in range(4):
        pieces.append((cont[i] + cont[i ^ 1]) * (cont[i] + cont[i ^ 2]) / comb)

    return 2 * sum(
        obs * math.log(obs / (exp + _SMALL) + _SMALL)
        for obs, exp in zip(cont, pieces)
    )

def kollo(
    content,
    query=None,
    left=5,
    right=5,
    span=None,
    number=20,
    metric="ll",
    target=0,
    output=[0],
    stopwords=None,
    case_sensitive=False,
):

    output = _fix_output(output)

    if span is not None:  # currently, you can't have a span and left+right.
        left = -1
        right = -1

    compiled = _prepare_query(query, case_sensitive)

    if stopwords:
        with open(stopwords, "r") as fo:
            stopwords = set(i.strip().lower() for i in fo.readlines())

    out = defaultdict(list)
    matches = set()
    boundaries = []
    offsets = {}
    total_bytes = 0
    word_count = 0
    word_freqs = Counter()

    size = os.path.getsize(content)
    

    with open(content, "r") as fo:

        pbar = tqdm(ncols=120, unit="bytes", desc="Finding collocates", total=size, unit_scale=True)

        for i, line in enumerate(fo):
            num_bytes = len(bytes(line, "utf-8"))
            pbar.update(num_bytes)
            offsets[i] = total_bytes
            total_bytes += num_bytes
            line = line.strip()
            # empty line:
            if not line:
                boundaries.append(True)
                continue
            # xml element line
            elif line.startswith("<") and line.endswith(">") and "\t" not in line:
                tag = line.strip(" <>").split(" =")[0].strip().split()[0].lstrip("/")
                boundaries.append(tag)
                continue
            # it's a token:
            boundaries.append(False)
            word_count += 1
            pieces = line.strip().split("\t")
            target_token = pieces[target].strip()
            output_token = "/".join(pieces[x] for x in output).strip()
            if not case_sensitive:
                target_token = target_token.lower()
                output_token = output_token.lower()
            word_freqs[output_token] += 1
            if not query:
                continue
            if _is_match(compiled, target_token, case_sensitive, stopwords):
                matches.add(i)

        pbar.close()

        fo.seek(0)
        total_lines = i

        span_size = 0

        if query:
            pbar = tqdm(ncols=120, unit="match", desc="Building match contexts", total=len(matches))
            window_size = None
            for match in sorted(matches):
                seeker, start, end, sent_len = _get_start_and_end(
                    match, left, right, span, boundaries, total_lines, offsets
                )
                if sent_len is not None:
                    span_size += sent_len
                fo.seek(seeker)
                base = int(start)
                for no, line in enumerate(fo):
                    check = line.strip()
                    actual_lineno = no + start
                    if (
                        not check
                        or "\t" not in check
                        or (check.startswith("<") and check.endswith(">"))
                    ):
                        continue
                    if actual_lineno >= end + 1:
                        break
                    pieces = [i.strip() for i in line.strip().split("\t")]
                    needed = tuple(pieces)
                    out[match].append(needed)

                pbar.update()
            pbar.close()

            if span and span_size:
                window_size = (span_size / len(matches)) - 1.0
        else:
            current = 0
            pbar = tqdm(ncols=120, unit="line", desc="Dividing into spans", total=total_lines)
            for i, line in enumerate(fo):
                line = line.strip()
                if not line:
                    pbar.update()
                    continue
                if span and boundaries[i] == span:
                    current += 1
                    pbar.update()
                    continue
                elif not span and isinstance(boundaries[i], str):
                    current += 1
                    pbar.update()
                    continue
                pieces = [i.strip() for i in line.strip().split("\t")]
                needed = tuple(pieces)
                out[current].append(needed)
                pbar.update()

            if span:
                window_size = (sum(len(x) for x in out.values()) / len(out)) - 1.0

            pbar.close()

    window_size = _get_window_size(left, right, window_size)

    metrics = {
        "ll": _likelihood_ratio,
        "ld": _log_dice,
        "mi3": _mi3,
        "mi": _mi,
        "t": _tscore,
        "z": _zscore,
    }

    sents = list(out.values())

    bigrams = from_words(sents, compiled, target, output, case_sensitive, stopwords)

    results = Counter()

    pbar = tqdm(ncols=120, unit="collocate", desc="Scoring collocates", total=len(bigrams))

    for (w1, w2), n in bigrams.items():

        try:
            adjusted = n / window_size
        except Exception as error:
            raise error

        if adjusted < 1.0:
        #    print("ADJUSTED SMALL", w1, w2, adjusted)
            adjusted = 1.0
        w1_freq = max(word_freqs[w1], adjusted)
        w2_freq = max(word_freqs[w2], adjusted)

        # print('CALCULATING', w1, w2, n, adjusted, w1_freq, w2_freq)

        score = 0
        if adjusted > 0.000000:
            score = metrics[metric](adjusted, (w1_freq, w2_freq), word_count)
        results[(w1, w2)] = score
        pbar.update()

    pbar.close()

    to_show = number if number != -1 else len(results)

    print("\n===========\nRESULTS\n===========\n")
    for k, v in results.most_common(to_show):
        k = " :: ".join(k)
        print(f"{k}\t{v:.4f}".expandtabs(30))


if __name__ == "__main__":
    from .cli import _parse_cmd_line

    kwargs = _parse_cmd_line()
    # print("KWARGS", kwargs)
    kollo(**kwargs)
