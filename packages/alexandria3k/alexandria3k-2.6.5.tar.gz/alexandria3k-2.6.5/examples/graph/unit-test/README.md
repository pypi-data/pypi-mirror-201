Query unit test using [rdbunit](https://github.com/dspinellis/rdbunit)

Run them from the parent directory with a command such as
```sh
for i in unit-test/*.rdbu ; do
  rdbunit -d sqlite $i | sqlite3
done
```
