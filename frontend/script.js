// URL base da API. Se mudar a porta/host do backend, ajuste aqui.
const API_URL = "http://127.0.0.1:8000";

const formCadastro = document.getElementById("form-cadastro");
const formLogin = document.getElementById("form-login");
const btnSair = document.getElementById("btn-sair");
const campoCpf = document.getElementById("cpf");
const campoPlaca = document.getElementById("placa");

// ---------- CADASTRO ----------
if (campoPlaca){
  campoPlaca.addEventListener("paste", function(event) {
    const valorColado = event.clipboardData.getData("text");
    const placaColada = valorColado.replace(/[^a-zA-Z0-9]/g, "").toUpperCase();
    const placaLimitada = placaColada.slice(0, 7);
    event.preventDefault();
    campoPlaca.value = placaLimitada;
    if (!/^[A-Z]{3}[0-9][A-Z][0-9]{2}$/.test(placaLimitada)) {
     campoPlaca.value = "";
    return;
}
  });
  campoPlaca.addEventListener("input", function(event){
    const valor = campoPlaca.value;
    const placa = valor.replace(/[^a-zA-Z0-9]/g, "").toUpperCase();
    const letraMaiuscula = placa.toUpperCase();
    const placaLimitada = letraMaiuscula.slice(0, 7);
    campoPlaca.value = placaLimitada;

    if (placaLimitada.length >= 1 && !/[A-Z]/.test(placaLimitada[0])) {
  campoPlaca.value = placaLimitada.slice(0, -1);
  return;
}
    if (placaLimitada.length >= 2 && !/[A-Z]/.test(placaLimitada[1])) {
  campoPlaca.value = placaLimitada.slice(0, -1);
  return;
}
if (placaLimitada.length >= 3 && !/[A-Z]/.test(placaLimitada[2])) {
  campoPlaca.value = placaLimitada.slice(0, -1);
  return;
}
if (placaLimitada.length >= 4 && !/[0-9]/.test(placaLimitada[3])) {
  campoPlaca.value = placaLimitada.slice(0, -1);
  return;
}
if (placaLimitada.length >= 5 && !/[A-Z]/.test(placaLimitada[4])) {
  campoPlaca.value = placaLimitada.slice(0, -1);
  return;
}
if (placaLimitada.length >= 6 && !/[0-9]/.test(placaLimitada[5])) {
  campoPlaca.value = placaLimitada.slice(0, -1);
  return;
}
if (placaLimitada.length >= 7 && !/[0-9]/.test(placaLimitada[6])) {
  campoPlaca.value = placaLimitada.slice(0, -1);
  return;
}
 });
}
if (campoCpf) {
  campoCpf.addEventListener("input", function(event){
    const valor = campoCpf.value;
    const cpf = valor.replace(/\D/g, "");

    if (cpf.length <=3){
      campoCpf.value = cpf;
      return;
    }
    if (cpf.length <=6){
      const primeiraParte = cpf.slice(0, 3);
      const segundaParte = cpf.slice(3);
      campoCpf.value = primeiraParte + "." + segundaParte;
      return;
    }
    if (cpf.length <=9){
      const primeiraParte = cpf.slice(0, 3);
      const segundaParte = cpf.slice(3, 6);
      const terceiraParte = cpf.slice(6);
      campoCpf.value = primeiraParte + "." + segundaParte + "." + terceiraParte;
      return;
      
    }
    const primeiraParte = cpf.slice(0, 3);
    const segundaParte = cpf.slice(3, 6);
    const terceiraParte = cpf.slice(6, 9);
    const quartaParte = cpf.slice(9);
    const cpfFormatado = primeiraParte + "." + segundaParte + "." + terceiraParte + "-" + quartaParte;
    campoCpf.value = cpfFormatado;
  });
}

if (formCadastro) {
  formCadastro.addEventListener("submit", async (e) => {
    e.preventDefault();
    const mensagem = document.getElementById("mensagem");
    mensagem.textContent = "";

    const dados = {
      nome: document.getElementById("nome").value,
      email: document.getElementById("email").value,
      senha: document.getElementById("senha").value,
    }

    try {
      const resposta = await fetch(`${API_URL}/cadastro`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
      })

      if (!resposta.ok) {
        const erro = await resposta.json();
        throw new Error(erro.detail || "Erro ao cadastrar");
      }

      mensagem.textContent = "Conta criada! Redirecionando para o login...";
      mensagem.className = "mensagem sucesso";
      setTimeout(() => (window.location.href = "index.html"), 1200);
    } catch (erro) {
      mensagem.textContent = erro.message;
      mensagem.className = "mensagem erro";
    }
  })
}

// ---------- LOGIN ----------
if (formLogin) {
  formLogin.addEventListener("submit", async (e) => {
    e.preventDefault();
    const mensagem = document.getElementById("mensagem");
    mensagem.textContent = "";

    // O endpoint /login espera dados como form-data (padrão OAuth2 do FastAPI)
    const corpo = new URLSearchParams();
    corpo.append("username", document.getElementById("email").value);
    corpo.append("password", document.getElementById("senha").value);

    try {
      const resposta = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: corpo,
      });

      if (!resposta.ok) {
        const erro = await resposta.json();
        throw new Error(erro.detail || "Erro ao entrar");
      }

      const dados = await resposta.json();
      localStorage.setItem("token", dados.access_token);

      mensagem.textContent = "Login realizado! Redirecionando...";
      mensagem.className = "mensagem sucesso";
      setTimeout(() => (window.location.href = "painel.html"), 800);
    } catch (erro) {
      mensagem.textContent = erro.message;
      mensagem.className = "mensagem erro";
    }
  });
}

// ---------- PAINEL (área protegida) ----------
async function carregarPainel() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  try {
    const resposta = await fetch(`${API_URL}/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!resposta.ok) throw new Error("Sessão expirada");

    const usuario = await resposta.json();
    document.getElementById("nome-usuario").textContent = usuario.nome;
  } catch {
    localStorage.removeItem("token");
    window.location.href = "index.html";
  }
}

if (btnSair) {
  btnSair.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "index.html";
  });
  carregarPainel();
}

// 👉 Ponto de expansão: novas chamadas à API (suas próximas funcionalidades)
// seguem o mesmo padrão: fetch(`${API_URL}/sua-rota`, { headers: { Authorization: `Bearer ${token}` } })
