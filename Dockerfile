FROM python:3
COPY ["cc-lookup/cc_lookup.py", "/opt/cc-lookup/"]
COPY ["cc-lookup/lookup.py", "/opt/cc-lookup"]
COPY ["cc-lookup/requirements.txt", "/opt/cc-lookup"]
RUN pip install --no-cache-dir -r /opt/cc-lookup/requirements.txt
WORKDIR /opt/cc-lookup/
CMD [ "python", "/opt/cc-lookup/cc_lookup.py" ]