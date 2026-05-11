Vue.component("project-card", {
  name: "project-card",
  props: {
    tags: {
      type: Array,
      default: () => ["tag1", "tag2", "tag3"],
    },
    title: {
      type: String,
      default: "This is a title by default",
    },
    description: {
      type: String,
      default:
        "Lorem ipsum dolor, sit amet consectetur adipisicing elit. Earum, aspernatur. Aliquid deleniti impedit, quisquam, velit ad utreiciendis provident voluptatem sapiente optio recusandae, est necessitatibus autem dolores quos quibusdam? Amet!",
    },
    author: {
      type: String,
      default: "unknown",
    },
    image: {
      type: String,
      default: "../assets/imgs/projet-default.png",
    },
  },
  data: function () {
    return {
      // You can remove 'author', 'title', 'description', 'image' here if you handle defaults via props
    };
  },
  methods: {},
  template: `
<div class="project">
  <!-- left = logo du projet -->
  <div class="project-logo">
    <div class="logo">
      <img :src="image" alt="" />
    </div>
  </div>

  <div class="infos">
    <div class="project-name">
      <h2>{{ title }}</h2>
    </div>
    <div class="project-tags">
      <!-- the 'ul' of the tags is scrollable -->
      <div class="tag" v-for="tag in tags" :key="tag">{{ tag }}</div>
    </div>
    <div class="description"><p>{{ description }}</p></div>
    <div class="owner">Created by : <a href='/author/{{author}}'>  {{ author }} </a> </div>
  </div>
</div>
`,
});
