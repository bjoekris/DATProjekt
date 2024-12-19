//4
const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.send('Backend server running');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});


//6
let users = [];

app.use(bodyParser.json());

app.post('/register', async (req, res) => {
    const { username, password } = req.body;

    const userExists = users.find(user => user.username === username);
    if (userExists) {
        return res.status(400).json({ message: 'User already exists' });
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const newUser = { username, password: hashedPassword };
    users.push(newUser);

    res.status(201).json({ message: 'User created' });
});

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    const user = { username, password };

    if (!user) {
        return res.status(404).json({ message: 'User not found' });
    }

    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
        return res.status(400).json({ message: 'Invalid credentials' });
    }

    const token = jwt.sign ({ userId: user.id }, 'yourSecretKey', { expiresIn: '1h' });

    res.json({ token });

});