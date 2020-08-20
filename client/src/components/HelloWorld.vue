<template>
  <div class="hello">
    <h1>Taco <em>OR</em> Burrito</h1>
    <p>
      Cut and paste the url of a taco or burrito picture:
    </p>
    <p>
      <input id="urlinput" type="text" v-model="url"  /> <button v-on:click="predict()" v-if="url.length > 0">Predict!</button>
    </p>
    <p>
      <img :src="url" />
    </p>
    <p>
      {{ url }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data: () => {
    return {
      url: "",
      processing: false
    }
  },
  methods: {
    predict: async function () {
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

      console.log(options)

      const response = await fetch(endpoint, options)
      console.log(response)
      const prediction = await response.json()
      console.log(prediction)

    }    
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
