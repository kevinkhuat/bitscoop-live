umask 002


export CLICOLOR=1
export GREP_OPTIONS="--color=auto"
export LS_COLORS="di=32:fi=0:ln=31:ex=35"
export PS1="\u@\h:\W $ "
export TIME_STYLE=long-iso


export PATH=$HOME/bin:$PATH
export PATH=$PATH:/opt/nginx/sbin
export PATH=$PATH:/opt/passenger/bin
export PATH=$PATH:/opt/redis/bin


alias ls="ls --color"
alias ll="ls -al --color"
alias dir="ls -Fhl --color"
