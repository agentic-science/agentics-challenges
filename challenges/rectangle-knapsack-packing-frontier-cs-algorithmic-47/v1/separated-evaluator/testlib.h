#ifndef FRONTIER_MIN_TESTLIB_H
#define FRONTIER_MIN_TESTLIB_H
#include <bits/stdc++.h>

enum TResult { _ok, _wa, _pe, _fail, _points };

static std::string format(const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    va_list ap2;
    va_copy(ap2, ap);
    int n = std::vsnprintf(nullptr, 0, fmt, ap);
    va_end(ap);
    if (n < 0) {
        va_end(ap2);
        return std::string(fmt);
    }
    std::string s((size_t)n, '\0');
    std::vsnprintf(s.data(), s.size() + 1, fmt, ap2);
    va_end(ap2);
    return s;
}

struct pattern {
    std::string pat;
    explicit pattern(const std::string &p) : pat(p) {}
    bool matches(const std::string &s) const {
        try {
            return std::regex_match(s, std::regex(pat));
        } catch (...) {
            return true;
        }
    }
};

static int exit_code(TResult r) {
    if (r == _ok) return 0;
    if (r == _points) return 7;
    return 1;
}

[[noreturn]] static void quit_message(TResult r, const std::string &message) {
    std::fprintf(stderr, "%s\n", message.c_str());
    std::exit(exit_code(r));
}

[[noreturn]] static void quitf(TResult r, const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    va_list ap2;
    va_copy(ap2, ap);
    int n = std::vsnprintf(nullptr, 0, fmt, ap);
    va_end(ap);
    std::string s;
    if (n < 0) {
        s = fmt;
    } else {
        s.assign((size_t)n, '\0');
        std::vsnprintf(s.data(), s.size() + 1, fmt, ap2);
    }
    va_end(ap2);
    quit_message(r, s);
}

[[noreturn]] static void quitp(double points, const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    va_list ap2;
    va_copy(ap2, ap);
    int n = std::vsnprintf(nullptr, 0, fmt, ap);
    va_end(ap);
    std::string s;
    if (n < 0) {
        s = fmt;
    } else {
        s.assign((size_t)n, '\0');
        std::vsnprintf(s.data(), s.size() + 1, fmt, ap2);
    }
    va_end(ap2);
    if (s.empty()) s = format("points %.10f", points);
    quit_message(_points, s);
}

[[noreturn]] static void quitp(double points, const std::string &message = "") {
    if (message.empty()) quit_message(_points, format("points %.10f", points));
    quit_message(_points, message);
}

[[noreturn]] static void quitp(int points, const std::string &message = "") {
    quitp((double)points, message);
}

class InStream {
public:
    std::ifstream input;
    std::string name;

    void open(const char *path) {
        name = path;
        input.open(path, std::ios::in | std::ios::binary);
        if (!input) quitf(_fail, "cannot open %s", path);
    }

    bool eof() {
        skipBlanks();
        return input.peek() == EOF;
    }

    void skipBlanks() {
        while (input) {
            int c = input.peek();
            if (c == EOF || !std::isspace((unsigned char)c)) return;
            input.get();
        }
    }

    bool seekEof() {
        skipBlanks();
        return input.peek() == EOF;
    }

    char curChar() {
        int c = input.peek();
        return c == EOF ? '\0' : (char)c;
    }

    char readChar() {
        char c;
        if (!input.get(c)) quitf(_pe, "unexpected EOF while reading char");
        return c;
    }

    void readSpace() {
        char c = readChar();
        if (!std::isspace((unsigned char)c)) quitf(_pe, "expected whitespace");
    }

    void readEoln() {
        char c = readChar();
        if (c == '\r') {
            if (curChar() == '\n') readChar();
            return;
        }
        if (c != '\n') quitf(_pe, "expected end of line");
    }

    std::string readTokenRaw() {
        skipBlanks();
        std::string s;
        while (input) {
            int c = input.peek();
            if (c == EOF || std::isspace((unsigned char)c)) break;
            s.push_back((char)input.get());
        }
        if (s.empty()) quitf(_pe, "expected token");
        return s;
    }

    std::string readToken() { return readTokenRaw(); }
    std::string readToken(const std::string &, const char * = nullptr) { return readTokenRaw(); }
    std::string readToken(const char *) { return readTokenRaw(); }
    std::string readWord() { return readTokenRaw(); }

    std::string readString() {
        std::string s;
        while (input) {
            int c = input.peek();
            if (c == EOF) break;
            if (c == '\r') {
                input.get();
                if (input.peek() == '\n') input.get();
                break;
            }
            if (c == '\n') { input.get(); break; }
            s.push_back((char)input.get());
        }
        return s;
    }
    std::string readString(const std::string &, const char * = nullptr) { return readString(); }
    std::string readString(const char *, const char * = nullptr) { return readString(); }

    std::string readLine() { return readString(); }

    long long readLong() {
        std::string tok = readTokenRaw();
        size_t pos = 0;
        long long v = 0;
        try {
            v = std::stoll(tok, &pos);
        } catch (...) {
            quitf(_pe, "expected integer, got %s", tok.c_str());
        }
        if (pos != tok.size()) quitf(_pe, "expected integer, got %s", tok.c_str());
        return v;
    }

    long long readLong(long long l, long long r, const char * = nullptr) {
        long long v = readLong();
        if (v < l || v > r) quitf(_wa, "integer %lld outside [%lld,%lld]", v, l, r);
        return v;
    }
    long long readLong(long long l, long long r, const std::string &) { return readLong(l, r); }

    int readInt() { return (int)readLong(); }
    int readInt(int l, int r, const char * = nullptr) {
        long long v = readLong(l, r);
        return (int)v;
    }
    int readInt(int l, int r, const std::string &) { return readInt(l, r); }
    int readInteger() { return readInt(); }
    int readInteger(int l, int r, const char * = nullptr) { return readInt(l, r); }
    int readInteger(int l, int r, const std::string &) { return readInt(l, r); }

    double readDouble() {
        std::string tok = readTokenRaw();
        size_t pos = 0;
        double v = 0.0;
        try {
            v = std::stod(tok, &pos);
        } catch (...) {
            quitf(_pe, "expected double, got %s", tok.c_str());
        }
        if (pos != tok.size()) quitf(_pe, "expected double, got %s", tok.c_str());
        return v;
    }
    double readDouble(double l, double r, const char * = nullptr) {
        double v = readDouble();
        if (v < l || v > r) quitf(_wa, "double %.17g outside [%.17g,%.17g]", v, l, r);
        return v;
    }
    double readDouble(double l, double r, const std::string &) { return readDouble(l, r); }
    double readReal() { return readDouble(); }
    double readReal(double l, double r, const char * = nullptr) { return readDouble(l, r); }
};

static InStream inf, ouf, ans;

static void registerTestlibCmd(int argc, char *argv[]) {
    if (argc < 4) quitf(_fail, "checker expects input, output, and answer paths");
    inf.open(argv[1]);
    ouf.open(argv[2]);
    ans.open(argv[3]);
}

#endif
