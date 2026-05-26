#!/bin/bash

RESET="\u001b[0m"
GREEN="\u001b[32m"
RED="\u001b[31m"
YELLOW="\u001b[33m"

echo -e "${YELLOW}Checking packages...${RESET}"
sleep 2

bin=$PREFIX/bin
dir=$(pwd)

# ─── Git ───────────────────────────────────────────────
if [ -e "$bin/git" ]; then
  echo -e "${GREEN}[✓] git already installed, skipping.${RESET}"
else
  echo -e "${RED}[*] Installing git...${RESET}"
  pkg install git -y
  echo -e "${GREEN}[✓] Done.${RESET}"
fi

# ─── Python ────────────────────────────────────────────
if [ -e "$bin/python" ] || [ -e "$bin/python3" ]; then
  echo -e "${GREEN}[✓] python already installed, skipping.${RESET}"
else
  echo -e "${RED}[*] Installing python...${RESET}"
  pkg install python -y
  echo -e "${GREEN}[✓] Done.${RESET}"
fi

# ─── Bash ──────────────────────────────────────────────
if [ -e "$bin/bash" ]; then
  echo -e "${GREEN}[✓] bash already installed, skipping.${RESET}"
else
  echo -e "${RED}[*] Installing bash...${RESET}"
  pkg install bash -y
  echo -e "${GREEN}[✓] Done.${RESET}"
fi

# ─── Python packages (pip) ─────────────────────────────
echo -e "${YELLOW}[*] Installing Python packages via pip...${RESET}"
sleep 2

pip install --upgrade pip --quiet

PACKAGES="colorama bs4 requests pyfiglet tqdm"

for pkg_name in $PACKAGES; do
  echo -e "${YELLOW}    -> Installing $pkg_name ...${RESET}"
  pip install "$pkg_name" -q 2>/dev/null || pip install "$pkg_name" --break-system-packages -q 2>/dev/null
  echo -e "${GREEN}    [✓] $pkg_name done.${RESET}"
done

echo -e "${GREEN}[✓] All packages done!${RESET}"

# ─── Run ───────────────────────────────────────────────
echo -e "${YELLOW}[*] Running Tools...${RESET}"
sleep 2

python main.py
