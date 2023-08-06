# Run starknet-devnet locally

#### Create a Python environment
```
python3.9 -m venv ~/starknet-devnet-env
source ~/starknet-devnet-env/bin/activate
```

#### Install starknet dependencies
```
brew install gmp
CFLAGS=-I/opt/homebrew/opt/gmp/include LDFLAGS=-L/opt/homebrew/opt/gmp/lib pip install fastecdsa
pip install starknet-devnet
```

#### Install dev dependencies
```
git clone git@github.com:Shard-Labs/starknet-devnet.git
cd starknet-devnet
./scripts/install_dev_tools.sh
```

#### Testing: Compile contracts & run tests
```
./scripts/compile_contracts.sh
poetry run pytest -s -v test # To run all tests with verbose mode
poetry run pytest test/<TEST_FILE> # To run a single test
```

# Workflow
In order to test how changes in the starknet codebase affect the `starknet-devnet`, you can modify the code in `~/starknet-devnet-env/lib/python3.9/site-packages/starkware` and re-run tests.
This will be useful when we replace the native Python runner for our own Rust runner.
