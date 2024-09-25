const express = require('express');
const kue = require('kue');
const redis = require('redis');
const { promisify } = require('util');

// Create Redis client
const client = redis.createClient();

// Promisify Redis methods for async/await
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Create Kue queue
const queue = kue.createQueue();

// Express app
const app = express();
const port = 1245;

// Initialize the number of available seats and reservation status
let reservationEnabled = true;
const INITIAL_SEATS = 50;

// Function to reserve a seat in Redis
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Function to get the current available seats from Redis
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats, 10) : 0;
}

// Set the number of available seats to 50 when the application starts
reserveSeat(INITIAL_SEATS).then(() => {
  console.log(`Initial number of seats set to ${INITIAL_SEATS}`);
});

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  return res.json({ numberOfAvailableSeats: availableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    } else {
      return res.json({ status: 'Reservation in process' });
    }
  });

  // Log job completion or failure
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

// Route to process the queue
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();

    if (availableSeats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    const newAvailableSeats = availableSeats - 1;
    await reserveSeat(newAvailableSeats);

    if (newAvailableSeats === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
