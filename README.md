## Antonov124
- Um utilitário para busca de passagens aéreas.
- O resultado será algo parecido com o valor encontrado, datas de embarque/desembarque e origem/destino e link para acesso em arquivo de nome passagem_data.csv :
__R$307	307	2017-05-13	2017-05-15	GIG - Belo Horizonte – Confins (MG)	CNF__


## Como usar

* `config_origem.json` json com os aeroportos de origem;
* `config_destino.json` json com os aeroportos de destino;
* `config_params.json` json com as configurações de busca;

```js
//config_params.json
{
  //Data início possível viagem
  "start_day": 1, //
  "start_month": 4,
  "start_year": 2017,

  //Data fim possível viagem
  "end_day": 15,
  "end_month": 5,
  "end_year": 2017,

  //Intervalo mínimo no lugar destino
  "minimo_dias_no_lugar": 3,

  //Considerar outros intervalos diferentes de minimo_dias_no_lugar
  "periodo_de_dias_exatos":false,

  "ida_sexta_feira":true
  "ida_seg_qui":false,
  "volta_seg_qui":false,

  //Intervalo entre buscas no script
  "sleep":1
  //sufixo classe google utilizada para o menor valor
  "classe_google_menor_preco_sufixo":"-d-yb",
  //Salvar em banco
  "save_db":true
}
```

### Dependências
- http://phantomjs.org/
- python-pip python-dev

```sh
#com save_db == true
`docker pull rethinkdb`
`docker run -p 8088:8080 -p 28015:28015 --name antonov-rethink -v "$PWD:/data"  rethinkdb`
`bash config.sh `
`source env/bin/activate`
`python google.py`
```


```sh
#com save_db == false
`bash config.sh `
`source env/bin/activate`
`python google.py`
```
