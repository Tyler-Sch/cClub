

const protectedFetch = async (url, method, data = {}) => {
  const response = await fetch(
    url,
    {
      method: method,
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem('Authorization')
      },
      body: null
    }
  )
  const response_data = await response.json();
  // think I need something to catch an error here
  return response_data
}

export default protectedFetch;
