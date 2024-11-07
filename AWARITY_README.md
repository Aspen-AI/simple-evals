Steps to get simple-eval running

- `pip3 install venv` or `sudo apt install python3.12-venv`

- `mkdir .virtualenvs`
- `cd .virtualenvs`
- `python3 -m venv simple-evals`
- `source .virtualenvs/simple-evals/bin/activate`
- `pip3 install pandas jinja2 blobfile scipy human_eval anthropic openai`

Below works because it's a public repo
- `cd ~/GitHub`
- `git clone https://github.com/Aspen-AI/simple-evals.git`

`export OPENAI_API_KEY=sk-proj-ZwG...` (insert actual OPENAI key here)

Modify code in samples, e.g. in `simple-evals/sampler/o1_chat_completion_sampler.py` uncomment this line:

`api_key=os.environ.get("OPENAI_API_KEY")  # please set your API_KEY`

Finally, run

`python -m simple-evals.demo`
