document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("health-form");
  const tableBody = document.getElementById("table-body");

  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    renderTable([data]);
  });

  function renderTable(dataArray) {
    tableBody.innerHTML = "";

    dataArray.forEach((item, index) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${index + 1}</td>
        <td>${item.nome}</td>
        <td>${item.genero == 0 ? "Masculino" : "Feminino"}</td>
        <td>${item.idade}</td>
        <td>${item.altura}</td>
        <td>${item.peso}</td>
        <td>${["<1L", "1-2L", ">2L"][item.agua]}</td>
        <td>${["Nenhuma", "1-2d", "2-4d", "4-5d"][item.atividade_fisica]}</td>
        <td>${["Nunca", "Às vezes", "Sempre"][item.vegetais]}</td>
        <td>${["Não bebo", "Às vezes", "Freq.", "Sempre"][item.alcool]}</td>
        <td>${["Transp. Público", "Caminhada", "Moto", "Bicicleta", "Carro"][item.transporte]}</td>
      `;
      tableBody.appendChild(row);
    });
  }
});

function mapSelectValuesToLabels(dataList) {
  const mappings = {
    gender: { 0: "Masculino", 1: "Feminino" },
    family_history: { 1: "Sim", 2: "Não" },
    favc: { 1: "Sim", 0: "Não" },
    fcvc: { 0: "Nunca", 1: "Às vezes", 2: "Sempre" },
    ncp: { 0: "1-2", 1: "Três", 2: "Mais de 3" },
    caec: { 1: "Sim", 0: "Não" },
    smoke: { 1: "Sim", 0: "Não" },
    ch2o: { 0: "Menos de 1 litro", 1: "Entre 1-2 litros", 2: "Mais de 2 litros" },
    scc: { 1: "Sim", 0: "Não" },
    faf: {
      0: "Não faço",
      1: "1-2 dias",
      2: "2-4 dias",
      3: "4-5 dias"
    },
    tue: { 0: "0-2h", 1: "3-5h", 2: "Mais de 5h" },
    calc: {
      0: "Não bebo",
      1: "Às vezes",
      2: "Frequentemente",
      3: "Sempre"
    },
    transportation: {
      0: "Transporte Público",
      1: "Caminhada",
      2: "Moto",
      3: "Bicicleta",
      4: "Carro"
    },
    outcome: {
      0: "Peso Normal",
      1: "Abaixo do Peso",
      2: "Obesidade Grau I",
      3: "Obesidade Grau II",
      4: "Obesidade Grau III",
      5: "Acima do Peso Grau I",
      6: "Acima do Peso Grau II"
    }
  };

  return dataList.pessoas.map(item => {
    const newItem = { ...item };

    for (const key in mappings) {
      if (newItem.hasOwnProperty(key)) {
        const value = newItem[key];
        // Só aplica mapeamento se o valor for reconhecido
        newItem[key] = mappings[key].hasOwnProperty(value)
          ? mappings[key][value]
          : value;
      }
    }
 
    return newItem;
  });
}

/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/pessoas';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data = mapSelectValuesToLabels(data);
      data.forEach(item => insertList(  item.id,
                                                item.nome, 
                                                item.gender, 
                                                item.age,
                                                item.height,
                                                item.weight,
                                                item.family_history,
                                                item.favc,
                                                item.fcvc,
                                                item.ncp,
                                                item.caec,
                                                item.smoke,
                                                item.ch2o,
                                                item.scc,
                                                item.faf,
                                                item.tue,
                                                item.calc,
                                                item.transportation,
                                                item.outcome
                                              ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para limpar a tabela antes de recarregar os dados
  --------------------------------------------------------------------------------------
*/
const clearTable = () => {
  var table = document.getElementById('data-table');
  // Remove todas as linhas exceto o cabeçalho (primeira linha)
  while(table.rows.length > 1) {
    table.deleteRow(1);
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para recarregar a lista completa do servidor
  --------------------------------------------------------------------------------------
*/
const refreshList = async () => {
  clearTable();
  await getList();
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
// Carrega a lista apenas uma vez quando a página é carregada
document.addEventListener('DOMContentLoaded', function() {
  getList();
});




/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (gender, age, height,
                        weight, family_history, favc, 
                        fcvc, ncp, caec,
                        smoke, ch2o, scc, faf,
                        tue, calc, transportation,
                        nome
                      ) => {
    
  const formData = new FormData();
  formData.append('gender', gender);
  formData.append('age', age);
  formData.append('height', height);
  formData.append('weight', weight);
  formData.append('family_history', family_history);
  formData.append('favc', favc);
  formData.append('fcvc', fcvc);
  formData.append('ncp', ncp);
  formData.append('caec', caec);
  formData.append('smoke', smoke);
  formData.append('ch2o', ch2o);
  formData.append('scc', scc);
  formData.append('faf', faf);
  formData.append('tue', tue);
  formData.append('calc', calc);
  formData.append('transportation', transportation);
  formData.append('nome', nome);

  let url = 'http://127.0.0.1:5000/pessoa';
  return fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .then((data) => {
      return data; // Retorna os dados do paciente com o diagnóstico
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[1].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/pessoa?nome='+item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async (event) => {
  event.preventDefault();

  let nome = document.getElementById("nome").value;
  let gender = document.getElementById("gender").value;
  let age = document.getElementById("age").value;
  let height = document.getElementById("height").value;
  let weight = document.getElementById("weight").value;
  let family_history = document.getElementById("family_history").value;
  let favc = document.getElementById("favc").value;
  let fcvc = document.getElementById("fcvc").value;
  let ncp = document.getElementById("ncp").value;
  let caec = document.getElementById("caec").value;
  let smoke = document.getElementById("smoke").value;
  let ch2o = document.getElementById("ch2o").value;
  let scc = document.getElementById("scc").value;
  let faf = document.getElementById("faf").value;
  let tue = document.getElementById("tue").value;
  let calc = document.getElementById("calc").value;
  let transportation = document.getElementById("transportation").value;

  // Verifique se o nome do produto já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/pessoas?nome=${nome}`;
  fetch(checkUrl, {
    method: 'get'
  })
    .then((response) => response.json())
    .then(async (data) => {
      if (data.pessoas && data.pessoas.some(item => item.nome === nome)) {
        alert("Pessoa já está cadastrada.\nCadastre uma pessoa com um nome diferente ou atualize o existente.");
      } else if (nome === '') {
        alert("O nome da pessoa não pode ser vazio!");
      } else if (isNaN(gender) || isNaN(age) || isNaN(height) || isNaN(weight) || isNaN(family_history) || isNaN(favc) || isNaN(fcvc) || isNaN(ncp)
      || isNaN(caec) || isNaN(smoke) || isNaN(ch2o) || isNaN(scc) || isNaN(faf) || isNaN(tue) || isNaN(calc) || isNaN(transportation)) {
        alert("Todos os campos devem ser preenchidos!");
      } else {
        try {
          // Envia os dados para o servidor e aguarda a resposta com o diagnóstico
          const result = await postItem(gender, age, height,
                        weight, family_history, favc, 
                        fcvc, ncp, caec,
                        smoke, ch2o, scc, faf,
                        tue, calc, transportation,
                        nome);
            // Limpa o formulário
          document.getElementById("nome").value = "";
          document.getElementById("gender").value = "";
          document.getElementById("age").value = "";
          document.getElementById("height").value = "";
          document.getElementById("weight").value = "";
          document.getElementById("family_history").value = "";
          document.getElementById("favc").value = "";
          document.getElementById("fcvc").value = "";
          document.getElementById("ncp").value = "";
          document.getElementById("caec").value = "";
          document.getElementById("smoke").value = "";
          document.getElementById("ch2o").value = "";
          document.getElementById("scc").value = "";
          document.getElementById("faf").value = "";
          document.getElementById("tue").value = "";
          document.getElementById("calc").value = "";
          document.getElementById("transportation").value = "";
          
          // Recarrega a lista completa para mostrar o novo paciente com o diagnóstico
          await refreshList();
          
          // Mostra mensagem de sucesso com o diagnóstico
          // const diagnostico = result.outcome === 1 ? "DIABÉTICO" : "NÃO DIABÉTICO";
          // alert(`Paciente adicionado com sucesso!\nDiagnóstico: ${diagnostico}`);
          
          // Scroll para a tabela para mostrar o novo resultado
          // document.querySelector('.items').scrollIntoView({ 
          //   behavior: 'smooth', 
          //   block: 'center' 
          // });
          
        } catch (error) {
          console.error('Erro ao adicionar pessoa:', error);
          alert("Erro ao adicionar pessoa. Tente novamente.");
        }
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      alert("Erro ao verificar pessoa existente. Tente novamente.");
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (id, gender, age, height,
                        weight, family_history, favc, 
                        fcvc, ncp, caec,
                        smoke, ch2o, scc, faf,
                        tue, calc, transportation,
                        nome, outcome) => {
  var item = [id, gender, age, height,
                        weight, family_history, favc, 
                        fcvc, ncp, caec,
                        smoke, ch2o, scc, faf,
                        tue, calc, transportation,
                        nome, outcome];
  var table = document.getElementById('data-table');
  var row = table.insertRow();

  // Insere as células com os dados do paciente
  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  // Aplica styling baseado no diagnóstico
  // if (outcome === 1) {
  //   diagnosticCell.className = "diagnostic-positive";
  // } else {
  //   diagnosticCell.className = "diagnostic-negative";
  // }

  // Insere o botão de deletar
  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  removeElement();
}