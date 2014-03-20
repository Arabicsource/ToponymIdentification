ToponymIdentification
=====================


## Information on toponymic lists:

1. MuCjambuldan_RawList.txt:
  - 13,793 toponymic entities
  - includes simplified ranking for top toponyms in Ta*'r_i_h al-isl_am
  - includes relevant nisbas, if they are given in entries

2. MuCjambuldan_TopListCleanWithRepetitions.txt
  - 13,793 toponymic entities
  - only these toponyms

3. MuCjambuldan_TopListCleanWithoutRepetitions.txt
  - 12,568 toponymic entities
  - repetitions deleted (the same name may refer to different places; such cases unified)

4. MuCjambuldan_WorkingList.txt
  - 12,539 toponymic entitie analyzed
  - simple toponyms analyzed with Buckwalter (unidentifiable tagged as NOTFOUND)
  - compound toponyms (two and more words) are place in a separate section (tagged as COMPOUND)
  - the list gives a rather sugnificant number of toponyms that cannot be common words.
  - it also includes manually tagged (MANUAL) toponyms, since Buckwalter recognizes the most common toponyms like Baghdad, Dimashq, Khurasan, etc. (first pass: 50 toponyms if this kind, including the most frequent dozen)

## Additional functions:
- reformat texts, splitting long lines into short ones (~72 symbols per line); makes long files more mamageable in text editors
