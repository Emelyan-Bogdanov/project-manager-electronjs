Vue.component("left-big-menu", {
  name: "left-big-menu",
  props: {
    compName: {
      type: String,
      default: "Vecteurs",
    },
  },
  data: function () {
    return {
      members: [],
      hasProjects: false,
      assignedCount: 0,
      userId: null,
    };
  },
  async mounted() {
    try {
      const session = await window.electronAPI.checkSession();
      const userId = session.loggedIn && session.user ? session.user.id : null;
      this.userId = userId;
      if (userId) {
        const myWs = await window.electronAPI.getMyWorkspaces(userId) || [];
        this.hasProjects = myWs.length > 0;

        const memberMap = {};
        for (const ws of myWs) {
          const wsMembers = await window.electronAPI.getWorkspaceMembers(ws.id) || [];
          wsMembers.forEach(m => {
            if (m.id !== userId) {
              memberMap[m.id] = m;
            }
          });
        }
        this.members = Object.values(memberMap).map(m => ({
          id: m.id,
          name: m.name,
          url: m.avatar || "",
          userId: m.id,
        }));

        const assigned = await window.electronAPI.getAssignedTasks(userId) || [];
        this.assignedCount = assigned.length;
      }
    } catch (e) {
      console.error("Error loading sidebar:", e);
    }
  },
  methods: {
    logout: function () {
      if (window.electronAPI && window.electronAPI.logout) {
        window.electronAPI.logout().then(() => {
          window.electronAPI.navigate("src/templates/auth/login.html");
        });
      }
    },
  },
  template: `
    <div>
      <company-logo :compName="compName"></company-logo>

      <div class="sidebar-title">Menu</div>

      <side-menu-button
        biclass="bi-house-fill"
        count="0"
        span-text="Tableau de bord"
        url="dashboard.html"
      ></side-menu-button>

      <side-menu-button v-if="hasProjects"
        biclass="bi-check2-square"
        span-text="Tâches"
        url="tasks.html"
      ></side-menu-button>

      <side-menu-button v-if="userId"
        biclass="bi-person-check"
        :count="String(assignedCount)"
        span-text="Assignées"
        url="tasks.html?assigned=1"
      ></side-menu-button>

      <side-menu-button
        biclass="bi-envelope"
        span-text="Requetes"
        url="requests.html"
      ></side-menu-button>

      <sidebar-section-header :has-plus="false"></sidebar-section-header>

      <div class="tools">
        <side-menu-button
          biclass="bi-stack"
          span-text="Projets"
          url="projects.html"
        ></side-menu-button>

        <side-menu-button
          biclass="bi-files"
          span-text="Fichiers"
          url="files.html"
        ></side-menu-button>

        <side-menu-button
          biclass="bi-people"
          span-text="Utilisateurs"
          url="allUsers.html"
        ></side-menu-button>

        <side-menu-button
          biclass="bi-person"
          span-text="Profil"
          url="profile.html"
        ></side-menu-button>

        <side-menu-button
          biclass="bi-gear"
          span-text="Config"
          url="config.html"
        ></side-menu-button>
      </div>

      <sidebar-section-header title="Membres de projet"></sidebar-section-header>

      <div class="members">
        <sidebar-member-item
          v-for="m in members"
          :key="m.id"
          :url="m.url"
          :name="m.name"
          :user-id="m.userId"
        ></sidebar-member-item>
        <div v-if="!members.length" style="color:rgba(255,255,255,0.4);font-size:12px;padding:8px 16px;text-align:center;">
          Aucun membre
        </div>
      </div>

      <div class="sidebar-logout" style="margin-top: auto; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.08);">
        <a href="#" class="menu-link" @click.prevent="logout">
          <div class="menu-left">
            <i class="bi bi-box-arrow-left"></i>
            <span>Déconnexion</span>
          </div>
        </a>
      </div>
    </div>`,
});
