#ifndef AGENTICS_MINI_TESTLIB_H
#define AGENTICS_MINI_TESTLIB_H

#include <bits/stdc++.h>
using namespace std;

enum TResult { _ok, _wa, _pe, _fail };

static string vformat_agentics(const char* fmt, va_list ap) {
    va_list copy;
    va_copy(copy, ap);
    int needed = vsnprintf(nullptr, 0, fmt, copy);
    va_end(copy);
    if (needed < 0) return string(fmt);
    string out((size_t)needed, '\0');
    vsnprintf(out.data(), out.size() + 1, fmt, ap);
    return out;
}

static string format(const char* fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    string out = vformat_agentics(fmt, ap);
    va_end(ap);
    return out;
}

class InStream {
    ifstream file;
public:
    void open(const char* path) {
        file.open(path, ios::in | ios::binary);
        if (!file) {
            fprintf(stderr, "fail cannot open %s\n", path);
            exit(4);
        }
    }

    bool seekEof() {
        file >> ws;
        return file.peek() == EOF;
    }

    void readEoln() {
        if (file.peek() == '\r') file.get();
        if (file.peek() == '\n') file.get();
    }

    string readToken() {
        string s;
        if (!(file >> s)) {
            fprintf(stderr, "wrong answer unexpected EOF while reading token\n");
            exit(3);
        }
        return s;
    }

    string readWord() { return readToken(); }
    string readString() { return readToken(); }

    string readLine() {
        string s;
        if (!std::getline(file, s)) return string();
        if (!s.empty() && s.back() == '\r') s.pop_back();
        return s;
    }

    int readInt() { return (int)readLong(); }

    int readInt(int l, int r) {
        long long v = readLong();
        if (v < l || v > r) {
            fprintf(stderr, "wrong answer integer %lld outside [%d,%d]\n", v, l, r);
            exit(3);
        }
        return (int)v;
    }

    int readInt(int l, int r, const char*) { return readInt(l, r); }

    long long readLong() {
        long long v;
        if (!(file >> v)) {
            fprintf(stderr, "wrong answer unexpected EOF while reading integer\n");
            exit(3);
        }
        return v;
    }

    long long readLong(long long l, long long r) {
        long long v = readLong();
        if (v < l || v > r) {
            fprintf(stderr, "wrong answer integer %lld outside [%lld,%lld]\n", v, l, r);
            exit(3);
        }
        return v;
    }

    long long readLong(long long l, long long r, const char*) { return readLong(l, r); }

    vector<long long> readLongs(int n) {
        vector<long long> xs(n);
        for (int i = 0; i < n; i++) xs[i] = readLong();
        return xs;
    }

    double readDouble() {
        double v;
        if (!(file >> v)) {
            fprintf(stderr, "wrong answer unexpected EOF while reading double\n");
            exit(3);
        }
        return v;
    }
};

static InStream inf, ouf, ans;

static void registerTestlibCmd(int argc, char* argv[]) {
    if (argc < 4) {
        fprintf(stderr, "fail checker expects input output answer paths\n");
        exit(4);
    }
    inf.open(argv[1]);
    ouf.open(argv[2]);
    ans.open(argv[3]);
}

static void quitf(TResult result, const char* fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    string msg = vformat_agentics(fmt, ap);
    va_end(ap);
    const char* prefix = result == _ok ? "ok" : (result == _fail ? "fail" : "wrong answer");
    fprintf(stderr, "%s %s\n", prefix, msg.c_str());
    exit(result == _ok ? 0 : (result == _fail ? 4 : 3));
}

static void quitp(double points, const char* fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    string msg = vformat_agentics(fmt, ap);
    va_end(ap);
    fprintf(stderr, "points %.12g %s\n", points, msg.c_str());
    exit(7);
}

static void ensuref(bool cond, const char* fmt, ...) {
    if (cond) return;
    va_list ap;
    va_start(ap, fmt);
    string msg = vformat_agentics(fmt, ap);
    va_end(ap);
    fprintf(stderr, "fail %s\n", msg.c_str());
    exit(4);
}

#endif
