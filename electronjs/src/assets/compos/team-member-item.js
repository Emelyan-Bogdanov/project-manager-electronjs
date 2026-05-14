Vue.component("team-member-item", {
  name: "team-member-item",
  props: {
    avatar: { type: String, default: "" },
    name: { type: String, default: "Membre" },
    role: { type: String, default: "Role" },
  },
  computed: {
    initials() {
      return this.name
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0].toUpperCase())
        .join("");
    },
  },
  template: `
    <div class="team-member">
      <img v-if="avatar" :src="avatar" alt="" class="team-avatar" />
      <div v-else class="team-avatar team-avatar-placeholder">{{ initials || "M" }}</div>
      <div class="team-info">
        <div class="team-name">{{ name }}</div>
        <div class="team-role">{{ role }}</div>
      </div>
    </div>`,
});
