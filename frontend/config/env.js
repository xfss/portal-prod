'use strict'
module.exports = {
  NODE_ENV: JSON.stringify(process.env.ENVIRONMENT),
  BACKEND_URL: JSON.stringify(process.env.BACKEND_URL),
  AXIOS_TIMEOUT: process.env.AXIOS_TIMEOUT
}
