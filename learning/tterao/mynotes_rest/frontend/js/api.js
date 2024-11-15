/**
  * @brief Calls an API using GET method and returns the response as JSON.
  * @params endpoint: string - The API endpoint to fetch data from.
  * @returns {Promise<object|null>} - A promise that resolves to the JSON response or null if an error occurred.
  */
export async function fetchData(endpoint) {
  try {
    const response = await fetch(endpoint)
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const json = await response.json();
    return json
  } catch (error) {
    console.error(error)
    return null
  }
}

/**
  * @brief Calls an API using POST method and returns the response as JSON.
  * @params endpoint: string - The API endpoint to fetch data from.
  * @params data: object - The payload to be sent in the POST request.
  * @returns {Promise<object|null>} - A promise that resolves to the JSON response or null if an error occurred.
  */
export async function postData(endpoint, data) {

  const option = {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    }
  }

  try {
    const response = await fetch(endpoint, option)
    if (!response.ok) {
      throw new Error(`Response status:  ${response.status}`);
    }
    const json = await response.json();
    return json
  } catch (error) {
    console.error(error)
    return null
  }
}


/**
  * @brief Calls an API using DELETE method and returns the response as JSON.
  * @params endpoint: string - The API endpoint to fetch data from.
  * @returns {Promise<object|null>} - A promise that resolves to the JSON response or null if an error occurred.
  */
export async function deleteData(endpoint) {

  const option = {
    method: "DELETE",
    headers: {
      'Content-Type': 'application/json',
    }
  }

  try {
    const response = await fetch(endpoint, option)
    if (!response.ok) {
      throw new Error(`Response status:  ${response.status}`);
    }
    const json = await response.json();
    return json
  } catch (error) {
    console.error(error)
    return null
  }
}
