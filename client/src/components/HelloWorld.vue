<template>
  <div class="hello">
    <h1>Taco or Burrito?</h1>
    <p>
      Cut and paste the url of a taco or burrito picture:
    </p>
    <p>
      <input id="urlinput" type="text" v-model="url" /> 
      <button v-on:click="predict()" v-if="url.length > 0">Predict!</button>
    </p>
    <p v-if="result">I think it is a <span id="prediction">{{ result.prediction }}</span></p>
    <p id="time" v-if="result">(Took {{ result.time }} seconds)</p>
    <ul id="scores" v-if="result">
      <li v-for="key in Object.keys(result.scores)"
          :key="key">
          {{ key }}: {{ result.scores[key] }}
      </li>
    </ul>
    <p>
      <img id="itm" :src="url" />
    </p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data: () => {
    return {
      url: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Breakfast_burritos.jpg/250px-Breakfast_burritos.jpg",
      processing: false,
      result: null
    }
  },
  methods: {
    predict: async function () {
      this.prediction = null
      const endpoint = "http://localhost:7071/api/predict"

      const options = {
        method: "POST",
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json;charset=UTF-8"
        },
        body: JSON.stringify({
          image: this.url
        })
      }

      const response = await fetch(endpoint, options)
      this.result = await response.json()
    }    
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#itm {
  max-width:450px;
  max-height:450px;
  width: auto;
  height: auto;
}
#prediction {
  font-size: 26px;
  color: red;
  font-weight: bold;
}
#scores {
  list-style-type: circle;
}
#scores li {
  display: block;
  font-size: 12px;
  color: #636363;
}
#time {
  font-size: 12px;
  color: #636363;
}
#urlinput {
  width: 400px;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
