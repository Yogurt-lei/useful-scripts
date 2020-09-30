ARG ELK_VERSION

# https://www.docker.elastic.co/
FROM logstash:${ELK_VERSION}

RUN gem sources --remove https://rubygems.org/
RUN gem sources -a http://gems.ruby-china.com
RUN gem sources -l

# Add your logstash plugins setup here
RUN logstash-plugin install logstash-filter-multiline