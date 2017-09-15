ARG base_python_version
FROM python:$base_python_version

ENV DEBIAN_FRONTEND noninteractive

ENV REPOS /repos
ENV HOME /root
ENV WORKON_HOME $HOME/.virtualenvs
ENV RB_TUTORIAL_VENV_NAME meta
ENV RB_TUTORIAL_VENV $WORKON_HOME/$RB_TUTORIAL_VENV_NAME
ENV RB_TUTORIAL_USER rb_tutorial
ENV RB_TUTORIAL_PASSWORD rb_tutorial
ENV RB_TUTORIAL_REPO $REPOS/rb_tutorial

ENV EDITOR vim

# Default docker just uses /bin/sh which makes virtualenv scripts rough
SHELL ["/bin/bash", "-c"]
RUN apt-get update \
 && apt-get -qq install \
    apt-utils \
    debhelper \
    dh-virtualenv \
    dpkg-dev \
    graphviz \
    htop \
    postgresql-client \
    sudo \
    vim \
    wget  \
 && useradd -ms /bin/bash -p $RB_TUTORIAL_PASSWORD $RB_TUTORIAL_USER \
 && wget --quiet -O /usr/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
 && chmod 0755 /usr/bin/wait-for-it \
 && ln -s $RB_TUTORIAL_REPO/provision/docker/rb_tutorial/docker-entrypoint.sh /usr/local/bin/dep \
 && wget --quiet -o get-pip.py https://bootstrap.pypa.io/get-pip.py \
 && python$base_python_version get-pip.py \
 && rm get-pip.py \
 && python$base_python_version -m pip install -q --no-input virtualenvwrapper vex ipdb pdbpp \
 && vex --python python2 -m $RB_TUTORIAL_VENV_NAME echo "Created virtualenv: $RB_TUTORIAL_VENV_NAME" \
 && vex --path $RB_TUTORIAL_VENV pip install -q -U pip make-deb\
 && echo $RB_TUTORIAL_VENV_NAME > .venv

COPY . $RB_TUTORIAL_REPO
WORKDIR $RB_TUTORIAL_REPO

# Install project
RUN vex $RB_TUTORIAL_VENV_NAME pip install -q -e .[all]

# cleanup
RUN rm -rf /var/cache/apt/* /var/lib/apt/lists/* \
 && chmod 755 /usr/local/bin/dep

# This probably shouldn't be changed
ENTRYPOINT ["/usr/local/bin/dep"]

# This should probably be changed
CMD ["/bin/bash"]