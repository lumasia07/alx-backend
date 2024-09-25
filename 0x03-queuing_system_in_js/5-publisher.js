import redis from 'redis';

const publisher = redis.createClient();

publisher.on('connect', () => {
  console.log('Redis client connected to the server');

  const publisher = redis.createClient();

  publisher.on('connect', () => {
    console.log('Redis client connected to the server');
  });
  
  publisher.on('error', (err) => {
    console.log(`Redis client not connected to the server: ${err.message}`);
  });

  function publishMessage(message, time) {
    setTimeout(() => {
      console.log(`About to send ${message}`);
      publisher.publish('holberton school channel', message);
    }, time);
  }

  publishMessage('Holberton School is cool!', 100);
  publishMessage('Learning Redis with Node.js', 200);
  publishMessage('KILL_SERVER', 300);
  
});