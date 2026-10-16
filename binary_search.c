/*
 * Binary Search (Divide and Conquer)
 * ------------------------------------------------------------
 * Contains:
 *   1. binary_search_iter() - iterative version
 *   2. binary_search_rec()  - recursive (divide & conquer) version
 *   3. linear_search()      - baseline for comparison
 *   4. trace_search()       - step-by-step visual demonstration
 *   5. run_tests()          - self-checking test cases
 *   6. benchmark()          - comparison counts: binary vs linear
 *
 * Compile : gcc -Wall -Wextra -O2 -o binary_search binary_search.c -lm
 * Run     : ./binary_search            (demo with key = 23)
 *           ./binary_search 56         (demo with your own key)
 *           ./binary_search 40 5 8 12 16 23 38 56 72 91
 *                                      (key first, then your own SORTED array)
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

static long cmp_count = 0;               /* counts key comparisons */

/* ---------- 1. Iterative binary search: O(log n) time, O(1) space ---------- */
int binary_search_iter(const int a[], int n, int key)
{
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;    /* avoids overflow of (lo+hi)/2 */
        cmp_count++;
        if (a[mid] == key)      return mid;
        else if (a[mid] < key)  lo = mid + 1;   /* discard left half  */
        else                    hi = mid - 1;   /* discard right half */
    }
    return -1;                           /* key not present */
}

/* ---------- 2. Recursive version: divide, conquer, (no combine step) ------- */
int binary_search_rec(const int a[], int lo, int hi, int key)
{
    if (lo > hi) return -1;              /* base case: empty range */
    int mid = lo + (hi - lo) / 2;        /* DIVIDE  */
    cmp_count++;
    if (a[mid] == key) return mid;
    if (a[mid] < key)                    /* CONQUER one half only */
        return binary_search_rec(a, mid + 1, hi, key);
    return binary_search_rec(a, lo, mid - 1, key);
}

/* ---------- 3. Linear search (baseline) ------------------------------------ */
int linear_search(const int a[], int n, int key)
{
    for (int i = 0; i < n; i++) {
        cmp_count++;
        if (a[i] == key) return i;
    }
    return -1;
}

/* ---------- 4. Visual step-by-step trace ----------------------------------- */
void trace_search(const int a[], int n, int key)
{
    int lo = 0, hi = n - 1, step = 0;
    printf("\n=== Searching for key = %d in %d elements ===\n", key, n);

    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        step++;
        printf("\nStep %d: lo=%d  hi=%d  mid=%d  a[mid]=%d\n",
               step, lo, hi, mid, a[mid]);

        printf("  index : ");                         /* index row */
        for (int i = 0; i < n; i++) printf("%4d", i);
        printf("\n  value : ");                       /* value row; [..] = active range */
        for (int i = 0; i < n; i++) printf("%4d", a[i]);
        printf("\n  range : ");                       /* marker row */
        for (int i = 0; i < n; i++) {
            if (i == mid)                printf("   M");
            else if (i == lo && i == hi) printf("  LH");
            else if (i == lo)            printf("   L");
            else if (i == hi)            printf("   H");
            else if (i > lo && i < hi)   printf("   .");
            else                         printf("   x");   /* x = discarded */
        }
        printf("\n");

        if (a[mid] == key) {
            printf("  -> a[%d] == %d : FOUND at index %d after %d step(s)\n",
                   mid, key, mid, step);
            return;
        } else if (a[mid] < key) {
            printf("  -> %d < %d : discard left half, lo = mid+1 = %d\n",
                   a[mid], key, mid + 1);
            lo = mid + 1;
        } else {
            printf("  -> %d > %d : discard right half, hi = mid-1 = %d\n",
                   a[mid], key, mid - 1);
            hi = mid - 1;
        }
    }
    printf("\n  -> range is empty (lo=%d > hi=%d) : %d NOT FOUND after %d step(s)\n",
           lo, hi, key, step);
}

/* ---------- 5. Self-checking tests ----------------------------------------- */
static int check(const char *name, int got, int expected)
{
    printf("  [%s] %-34s got=%2d expected=%2d\n",
           got == expected ? "PASS" : "FAIL", name, got, expected);
    return got == expected;
}

int run_tests(void)
{
    int a[] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    int n = sizeof a / sizeof a[0], ok = 1;
    printf("\n=== Self tests ===\n");
    ok &= check("first element (iter)",  binary_search_iter(a, n, 2), 0);
    ok &= check("last element (iter)",   binary_search_iter(a, n, 91), 9);
    ok &= check("middle element (iter)", binary_search_iter(a, n, 23), 5);
    ok &= check("missing, too small",    binary_search_iter(a, n, 1), -1);
    ok &= check("missing, too large",    binary_search_iter(a, n, 100), -1);
    ok &= check("missing, in between",   binary_search_iter(a, n, 40), -1);
    ok &= check("recursive finds 56",    binary_search_rec(a, 0, n - 1, 56), 7);
    ok &= check("recursive misses 57",   binary_search_rec(a, 0, n - 1, 57), -1);
    ok &= check("single element, found", binary_search_iter(a, 1, 2), 0);
    ok &= check("empty array",           binary_search_iter(a, 0, 2), -1);
    printf("  Result: %s\n", ok ? "ALL TESTS PASSED" : "SOME TESTS FAILED");
    return ok;
}

/* ---------- 6. Benchmark: comparisons for worst-case search ---------------- */
void benchmark(void)
{
    long sizes[] = {10, 100, 1000, 10000, 100000, 1000000};
    printf("\n=== Comparisons for a worst-case (absent) key ===\n");
    printf("%10s %14s %14s %12s\n", "n", "linear", "binary", "floor(lg n)+1");
    for (int s = 0; s < 6; s++) {
        int n = (int)sizes[s];
        int *a = malloc(n * sizeof *a);
        if (!a) { perror("malloc"); return; }
        for (int i = 0; i < n; i++) a[i] = 2 * i;     /* even numbers, sorted */

        cmp_count = 0; linear_search(a, n, -1 + 2 * n); long lin = cmp_count;
        cmp_count = 0; binary_search_iter(a, n, -1 + 2 * n); long bin = cmp_count;
        printf("%10d %14ld %14ld %12d\n", n, lin, bin, (int)floor(log2(n)) + 1);
        free(a);
    }
}

int main(int argc, char *argv[])
{
    int def[] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    int *a = def, n = 10, key = 23;

    if (argc >= 2) key = atoi(argv[1]);
    if (argc >= 3) {                              /* user-supplied sorted array */
        n = argc - 2;
        a = malloc(n * sizeof *a);
        if (!a) { perror("malloc"); return 1; }
        for (int i = 0; i < n; i++) a[i] = atoi(argv[i + 2]);
        for (int i = 1; i < n; i++)
            if (a[i - 1] > a[i]) {
                fprintf(stderr, "Error: array must be sorted in ascending order.\n");
                return 1;
            }
    }

    trace_search(a, n, key);                      /* the visual demonstration */
    if (argc < 3) {                               /* extras only for default demo */
        trace_search(a, n, 40);                   /* an unsuccessful search */
        run_tests();
        benchmark();
    }
    if (a != def) free(a);
    return 0;
}
