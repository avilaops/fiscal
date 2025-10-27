// Cloudflare Worker para proxy reverso
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)

  // Target URL do container Azure
  const targetUrl = `http://fiscal-avila.eastus.azurecontainer.io:8000${url.pathname}${url.search}`

  // Clone request e modifica o host
  const modifiedRequest = new Request(targetUrl, {
    method: request.method,
    headers: request.headers,
    body: request.body,
    redirect: 'follow'
  })

  // Remove headers que podem causar problemas
  modifiedRequest.headers.delete('cf-connecting-ip')
  modifiedRequest.headers.delete('cf-ray')

  try {
    const response = await fetch(modifiedRequest)

    // Clone response e adiciona headers de segurança
    const modifiedResponse = new Response(response.body, response)
    modifiedResponse.headers.set('X-Powered-By', 'Cloudflare Workers')

    return modifiedResponse
  } catch (error) {
    return new Response(`Erro ao conectar: ${error.message}`, {
      status: 502,
      statusText: 'Bad Gateway'
    })
  }
}
