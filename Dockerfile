FROM python:3.11

# copy the content of the local src directory to the working directory
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# add wait-for-it.sh to wait for the database to be ready and make it executable
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh