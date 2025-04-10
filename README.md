# eZnapshot 🥷🏻🎒
## **A Serverless approach to take periodic snapshots of your NFT holders (Loyal users)**

This automated snapshot taker uses Caldera/Blockscout API and GitHub workflow (Currently exclusive for ZERѲ network)

---

## 1. Cloning the repo 🪣
```shell
git clone git clone https://github.com/eferbarn/eZnapshot
```

## 2. Make your desired customizations 🖌️
```shell
cd eZnapshot
nano Tokens.json
```

In this section, you need to enter your desired tokens based on the standard provided below. You can use any text editor instead of Nano.
#### Tokens.json example
```json
[
   {
     "name": "Agent ZERRO - S1E1",
     "symbol": "ZERROS1E1",
     "contract": "0x87470544d0009cde93891a073822c03a6930f876"
   },
   {
     "name": "Agent ZERRO - S1E2 | Shadows Emerge",
     "symbol": "ZERROS1E2",
     "contract": "0x572C9543574f581E6B1c0ac979B0bec2D094847A"
   }
]
```

## 3. Preparing the automation mechanism (Optional) 🤖
Before you do anything, look at this to help you understand the automation concept more easily.
https://github.com/AgentZERRO/Znapshot/actions

Now, you can skip this step if you don't need automation. However, if you do, modify the `AutoSnapshot.yml`([AutoSnapshot.yml](AutoSnapshot.yml)) and `Config.json`([Config.json](Config.json)) files according to your specific requirements.
```shell
mv .github/workflows/AutoSnapshot.yml.example .github/workflows/AutoSnapshot.yml
```
For example, if you’ve enabled the Automator mechanism, you need to update the cron interval under `on:schedule`, as well as the job related to the ‍`Load config interval`. Also, the `interval_cron` in `Config.json` should be updated accordingly.

Remember, to use the Automator section, you must also create a few **GitHub Secrets** for your repository based on your personal information — we’ll go over those together in the following steps.

> * `REPO_PAT`: A personal access token with access to r/w the content (Submit commits on your behalf) and mandatory metadata accesses
> * `GH_COMMIT_PAT`: It's precisely like `REPO_PAT`, and I’ve only separated the two for some of my checks. If you’d prefer, you can also use the same value as above for this one.
> * `GIT_USER_NAME` Your git username
> * `GIT_USER_EMAIL`: Your git user email
> * `GPG_PRIVATE_KEY`: The corresponding private key that is generated using your username and email by the `gpg` CLI tool on your local computer
> * `GPG_PASSPHRASE`
> * `GPG_KEY_ID`

### If you don't need automated, verified commits under your name on this repo and are fine with GitHub's bot submitting the commits, you can ignore all of this. Remove the `-S` flag from the `git push` commands and omit it in the automator file to turn off signed commits.

Instead of using your email and username, you can use GitHub's default bot identity for workflows.
* Username: `github-actions[bot]`
* Email: `github-actions[bot]@users.noreply.github.com`

## 4. Executional steps 🐍
#### Install requirements and dependencies
```shell
python -m pip install --upgrade pip
pip install -r requirements.txt	
```
#### Run
```
python -m main.py
python -m dashboard.py
```

This will build you a directory like what you see [here: AgentZERRO/Znapshot](https://github.com/AgentZERRO/Znapshot)
1. [Historical Data](https://github.com/AgentZERRO/Znapshot/tree/main/historical_data): This helps you to track all your periodic snapshots during the time
2. [Index.json](https://github.com/AgentZERRO/Znapshot/blob/main/index.json): A simple notary for indexing snapshots in Historical Data
3. [Pagination](https://github.com/AgentZERRO/Znapshot/tree/main/Pagination): A paginated version of results will save here
4. [Total.csv](https://github.com/AgentZERRO/Znapshot/blob/main/Total.csv) and [Total.json](https://github.com/AgentZERRO/Znapshot/blob/main/Total.json): A complete version of your holders' Leaderboard in a raw form
5. [Statistics.json](https://github.com/AgentZERRO/Znapshot/blob/main/Statistics.json): A small file that holds general statistical information
6. [Top 10 holders chart](https://github.com/AgentZERRO/Znapshot/blob/main/top_10_holders_chart.png)

---
[![MΞHDI ⧗](https://img.shields.io/badge/M%CE%9EHDI-Zerion-darkblue)](https://link.zerion.io/)
---