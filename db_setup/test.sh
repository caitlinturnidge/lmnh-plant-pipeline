source ../.env

sqlcmd -S $DB_HOST,$DB_PORT -U $DB_USER -P $DB_PASSWORD -Q "USE plants; SELECT * FROM s_beta.plant;"