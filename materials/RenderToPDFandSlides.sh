for x in `ls *.qmd`
   do
      echo File: $x
      quarto render $x --to pdf
      # quarto render $x 
      echo ---------------------
   done 
