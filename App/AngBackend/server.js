const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const mysql = require('mysql2');

const app = express();
const port = 3000;

app.use(cors({
    origin: 'http://localhost:4200',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true
  }));


app.options('*', cors());
app.use(bodyParser.json());

const db = mysql.createConnection({
    host: 'mysql93.unoeuro.com',
    user: 'bbksolutions_dk',
    password: 'cmfbeAtrkR5zBaF426x3',
    database: 'bbksolutions_dk_db'
});

db.connect((err) => {
    if (err) {
        console.error('Error connecting to database');
        return;
    }
    console.log('Connected to database');
});

app.get('/', (req, res) => {
  res.send('Backend server running');
});

let users = [];
app.use(bodyParser.json());

//register
app.post('/register', async (req, res) => {
    const { email, password } = req.body;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
        return res.status(400).json({ message: 'Invalid email address' });
    }

    if (!password || password.length < 6) {
        return res.status(400).json({ message: 'Password must be at least 6 characters long' });
    }

    const checkQuery = `SELECT * FROM Users WHERE UserEmail = ?`;
    db.query(checkQuery, [email], async (err, result) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Database error' });
        }

        if (result.length > 0) {
            return res.status(400).json({ message: 'A user with that email already exists' });
        }

        const hashedPassword = await bcrypt.hash(password, 10);


        const insertQuery = `INSERT INTO Users (UserEmail, UserPassword) VALUES (?, ?)`;
        db.query(insertQuery, [email, hashedPassword], (err, result) => {
            if (err) {
                console.error(err);
                return res.status(500).json({ message: 'Error registering user' });
            }

            res.status(201).json({ message: 'User created' });
        });
    });
});

//login
app.post('/login', async (req, res) => {
    const { email, password } = req.body;

    const query = `SELECT * FROM Users WHERE UserEmail = ?`;
    db.query(query, [email], async (err, result) => {
        if (err) {
            console.error(err);
            return res.status(500).json({ message: 'Database error' });
        }

        if (result.length === 0) {
            return res.status(404).json({ message: 'User not found' });
        }

        const user = result[0];

        const isMatch = await bcrypt.compare(password, user.UserPassword);
        if (!isMatch) {
            return res.status(400).json({ message: 'Invalid credentials' });
        }

        const token = jwt.sign({ userId: user.UserEmail }, 'yourSecretKey', { expiresIn: '1h' });
        res.json({ token });
    });

});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});