for letter in a b c d e f ; do
    python3 solvers/solve.py "in/$letter.in"  | tail -n +3 > "out/$letter.out"
done
