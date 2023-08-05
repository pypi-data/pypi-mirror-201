import numpy as np


def read_record(data, fmt):
    """Parse string to data given format."""
    token_to_type = {
        "s": str,
        "S": str,
        "d": int,
        "f": to_float,
        "e": to_float,
    }

    i = 0
    out = []
    for token in fmt.split(","):
        n = int(token[:-1].split(".")[0])
        tmp = data[i : i + n]
        tmp = tmp if token[-1] == "S" else tmp.strip()
        out.append(token_to_type[token[-1]](tmp) if tmp else None)
        i += n

    return out


def write_record(data, fmt, multi=False):
    """Return a list of record strings given format."""
    if not multi:
        data = [to_str(d, f) for d, f in zip(data, fmt)]
        out = [f"{''.join(data):80}\n"]

    else:
        n = len(data)
        ncol = len(fmt)
        data = [
            data[ncol * i : min(ncol * i + ncol, n)]
            for i in range(int(np.ceil(n / ncol)))
        ]

        out = []
        for d in data:
            d = [to_str(dd, f) for dd, f in zip(d, fmt)]
            out += [f"{''.join(d):80}\n"]

    return out


def to_float(s):
    """Convert variable string to float."""
    try:
        return float(s.replace("d", "e"))

    except ValueError:
        # It's probably something like "0.0001-001"
        significand, exponent = s[:-4], s[-4:]
        return float(f"{significand}e{exponent}")


def to_str(x, fmt):
    """Convert variable to string."""
    x = "" if x is None else x

    if not isinstance(x, str):
        # Special handling for floating point numbers
        if "f" in fmt:
            # Number of decimals is specified
            if "." in fmt:
                n = int(fmt[3:].split(".")[0])
                tmp = fmt.format(x)

                if len(tmp) > n:
                    return fmt.replace("f", "e").format(x)

                else:
                    return tmp

            # Let Python decides the format
            # n - 1 to leave a whitespace between values
            else:
                n = int(fmt[3:].split("f")[0])
                tmp = str(float(x))

                # If it's longer than n-1, use scientific notation
                if len(tmp) > n - 1:
                    fmt = f"{{:>{n}.{n - 7}e}}"

                    # Remove trailing zeros (e.g., "1.300e+07" -> "  1.3e+07")
                    left, right = fmt.format(x).split("e")
                    fmt = f"{{:>{len(left)}}}e{right}"

                    return fmt.format(str(float(left)))

                # If it's a scientific notation, make sure there is a decimal point
                elif "e" in tmp and "." not in tmp:
                    fmt = f" {{:>{n - 1}.1e}}"

                    return fmt.format(x)

                # Otherwise, display as is
                else:
                    fmt = f" {{:>{n - 1}}}"

                    return fmt.format(tmp)

        else:
            return fmt.format(x)

    else:
        return fmt.replace("g", "").replace("e", "").replace("f", "").format(x)
