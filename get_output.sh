#use: ./get_output.sh path/to/solver.py
for letter in a b c d e f ; do
    python3 "$i" "in/$letter.in"  | tail -n +3 > "out/$letter.out"
done
