#use: ./get_output.sh path/to/solver.py
for letter in a b c d e f ; do
    python "$1" "in/$letter.in"  | tail -n +3 > "out/$letter.out"
done
