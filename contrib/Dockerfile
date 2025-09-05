FROM ruby:3.3

WORKDIR /srv/jekyll

RUN gem install bundler -v 2.3.0

RUN gem install jekyll-scholar

COPY Gemfile ./
RUN bundle install

CMD [ "bundle", "exec", "jekyll", "serve" ]
