---
description: Insert one new dummy user into the database, with auto-generated name/email/password
argument-hint: (no arguments)
allowed-tools: Bash(venv/Scripts/python.exe:*)
---

Run this to create a brand-new dummy user in `spendly.db` with freshly generated field values that look like real user data (not a fixed/hardcoded user, and not blocked by any existing rows):

```bash
venv/Scripts/python.exe -c "
import random
from werkzeug.security import generate_password_hash
from database.db import init_db, get_db

init_db()

first_names = ['James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda',
               'David', 'Elizabeth', 'William', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
               'Thomas', 'Sarah', 'Daniel', 'Karen', 'Matthew', 'Nancy', 'Anthony', 'Lisa',
               'Priya', 'Aditya', 'Neha', 'Rahul', 'Ananya', 'Vikram']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
              'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
              'Clark', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King']
domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com']

first = random.choice(first_names)
last = random.choice(last_names)
name = f'{first} {last}'
email = f'{first.lower()}.{last.lower()}{random.randint(1, 9999)}@{random.choice(domains)}'
password = ''.join(random.choices('abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789', k=10))
password_hash = generate_password_hash(password)

conn = get_db()
conn.execute(
    'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
    (name, email, password_hash),
)
conn.commit()
conn.close()

print(f'name={name}')
print(f'email={email}')
print(f'password={password}')
"
```

After running it, give a short, plain-language summary for the student: confirm a new user row was inserted and show the generated name, email, and plaintext password (the password printed here is the only place it's visible — only the hash is stored). If the command errors, briefly say what failed and why (e.g. a UNIQUE constraint hit on the email, though it's unlikely given the random name/number combo).
