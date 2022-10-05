# general-stim

This is a general-purpose intracortical microstimulation (ICMS) script using the Intan RHX/S stimulation platform.

## Setup

Ensure the proper packages are installed. Most packages used are built-in, but `dotenv` is not. To install:

```bash
pip install dotenv
```

This script can be run on the same device as the Intan software (set `IP_ADDRESS` to `127.0.0.1` to use localhost) or on a separate device controlling the software over the Internet or a local network.

## Usage

To provide a user-friendly experience that doesn't involve editing the script or entering many arguments for each script run (and to efficiently preserve settings between runs), we use `.env` files. An example is provided (`.env.example`) for reference, complete with comments for documentation. Stim and TCP connection parameters should be entered within that file. To use the example as a base, rename it to `.env`:

```bash
mv .env.example .env
```

Then, run the script, optionally with the `-r` (or `--record`) argument to record the data to an env var-supplied recording location:

```bash
./stim.py [-r | --record]
```

## Credits

- Thomas Makin (Swarthmore College), Author
- Dadarlat Lab (Weldon School of Biomedical Engineering, Purdue University)
- Intan Technologies
