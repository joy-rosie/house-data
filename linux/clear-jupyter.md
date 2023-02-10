```sh
find . -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*' -exec jupyter nbconvert --clear-output --inplace {} \;
```