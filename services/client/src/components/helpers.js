

const protectedFetch = async (url, method, data = null) => {
  console.log(data);
  const response = await fetch(
    url,
    {
      method: method,
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        "Authorization": localStorage.getItem('Authorization')
      },
      body: (data != null) ? JSON.stringify(data) : null
    }
  )
  const response_data = await response.json();
  // think I need something to catch an error here
  return response_data
}

export default protectedFetch;


export function encodeData(data) {
    return Object.keys(data).map(function(key) {
        return [key, data[key]].map(encodeURIComponent).join("=");
    }).join("&");
}
