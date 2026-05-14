Vue.component("task-slide-panel", {
  props: {
    taskId: { type: Number, default: null },
    visible: { type: Boolean, default: false },
  },
  data() {
    return {
      task: null,
      loading: false,
      session: null,
      editing: false,
      blocks: [],
      showBlockMenu: null,
      saving: false,
      focusedBlock: null,
      titlePrompt: { visible: false, fileData: null, insertIdx: undefined, title: "" },
    };
  },
  watch: {
    taskId(n) {
      if (n && this.visible) this.loadTask(n);
    },
    visible(v) {
      if (v) {
        document.body.style.overflow = "hidden";
        if (this.taskId) this.loadTask(this.taskId);
      } else {
        document.body.style.overflow = "";
        this.task = null;
        this.blocks = [];
        this.editing = false;
        this.showBlockMenu = null;
        this.focusedBlock = null;
      }
    },
  },
  methods: {
    async loadTask(id) {
      if (!id) return;
      this.loading = true;
      try {
        const [task, session] = await Promise.all([
          window.electronAPI.getTask(id),
          window.electronAPI.checkSession(),
        ]);
        this.task = task;
        this.session = session;
        this.editing =
          session.loggedIn &&
          session.user &&
          session.user.id === task.authorId;
        this.parseBlocks(task.description || "");
      } catch (e) {
        console.error(e);
        this.task = null;
      } finally {
        this.loading = false;
      }
    },
    parseBlocks(desc) {
      try {
        const parsed = JSON.parse(desc);
        if (Array.isArray(parsed)) {
          this.blocks = parsed;
          return;
        }
      } catch {}
      this.blocks = desc
        ? [{ type: "text", content: `<p>${desc}</p>` }]
        : [];
    },
    get serialized() {
      return JSON.stringify(this.blocks);
    },
    addBlock(idx, type) {
      const block =
        type === "header"
          ? { type: "header", content: "" }
          : { type: "text", content: "" };
      this.blocks.splice(idx + 1, 0, block);
      this.showBlockMenu = null;
    },
    removeBlock(idx) {
      this.blocks.splice(idx, 1);
    },
    pickImage(insertIdx) {
      const input = document.createElement("input");
      input.type = "file";
      input.accept = "image/*";
      input.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => {
          this.titlePrompt = { visible: true, fileData: ev.target.result, insertIdx, title: "" };
          this.showBlockMenu = null;
        };
        reader.readAsDataURL(file);
      };
      input.click();
    },
    confirmImageTitle() {
      const title = this.titlePrompt.title || "";
      const block = { type: "image", src: this.titlePrompt.fileData, title };
      if (typeof this.titlePrompt.insertIdx === "number") {
        this.blocks.splice(this.titlePrompt.insertIdx + 1, 0, block);
      } else {
        this.blocks.push(block);
      }
      this.titlePrompt = { visible: false, fileData: null, insertIdx: undefined, title: "" };
    },
    onBlockInput(idx, e) {
      this.blocks[idx].content = e.target.innerHTML;
    },
    formatBlock(command) {
      document.execCommand(command, false, null);
    },
    async save() {
      this.saving = true;
      try {
        await window.electronAPI.updateTask(this.task.id, {
          description: this.serialized,
        });
        this.$emit("saved");
      } catch (e) {
        console.error(e);
      } finally {
        this.saving = false;
      }
    },
    close() {
      this.$emit("close");
    },
    initials(name) {
      return (name || "U")
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .map((p) => p[0].toUpperCase())
        .join("");
    },
  },
  template: `
    <div class="task-slide-overlay" v-if="visible" @click.self="close">
      <div class="task-slide-panel">
        <div class="slide-panel-header">
          <h3>{{ task ? task.title : 'Loading...' }}</h3>
          <div class="slide-panel-actions">
            <button v-if="editing" class="slide-btn save-btn" @click="save" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
            <button class="slide-btn close-btn" @click="close">&times;</button>
          </div>
        </div>

        <div v-if="loading" class="slide-loading">
          <div class="spinner-border" role="status"></div>
        </div>

        <div v-else-if="task" class="slide-panel-body">
          <div class="slide-meta">
            <span class="slide-type">{{ task.taskType === "advanced" ? "Advanced" : "Simple" }}</span>
            <span>{{ task.deadline || "No deadline" }}</span>
            <span>{{ task.status }}</span>
          </div>

          <div class="slide-author">
            <img v-if="task.authorAvatar" :src="task.authorAvatar" alt="" />
            <div v-else class="slide-author-placeholder">{{ initials(task.authorName) }}</div>
            <div>
              <strong>{{ task.authorName || "User" }}</strong>
              <p>Task owner</p>
            </div>
            <span v-if="editing" class="editing-badge">Editing</span>
          </div>

          <div class="slide-tags" v-if="task.tags && task.tags.length">
            <span v-for="t in task.tags" :key="t">{{ t }}</span>
          </div>

          <div class="slide-blocks">
            <div v-for="(block, idx) in blocks" :key="idx" class="block-wrapper">
              <div v-if="editing" class="block-divider">
                <button class="add-block-btn" @click.stop="showBlockMenu = showBlockMenu === idx ? null : idx">+</button>
                <div v-if="showBlockMenu === idx" class="block-menu">
                  <button @click="addBlock(idx, 'header')">Header</button>
                  <button @click="addBlock(idx, 'text')">Text</button>
                  <button @click="pickImage(idx)">Image</button>
                </div>
              </div>

              <div v-if="block.type === 'header'" class="block block-header" :class="{ editing }">
                <h2 v-if="!editing" v-html="block.content || 'Untitled'"></h2>
                <h2 v-else contenteditable="true"
                  @input="onBlockInput(idx, $event)"
                  @focus="focusedBlock = idx"
                  v-html="block.content"></h2>
                <button v-if="editing" class="block-remove" @click="removeBlock(idx)">&times;</button>
              </div>

              <div v-if="block.type === 'text'" class="block block-text" :class="{ editing }">
                <div v-if="editing && focusedBlock === idx" class="block-toolbar">
                  <button @click="formatBlock('bold')" title="Bold"><b>B</b></button>
                  <button @click="formatBlock('italic')" title="Italic"><i>I</i></button>
                  <button @click="formatBlock('underline')" title="Underline"><u>U</u></button>
                </div>
                <div v-if="!editing" class="text-content" v-html="block.content || ''"></div>
                <div v-else class="text-content editable" contenteditable="true"
                  @input="onBlockInput(idx, $event)"
                  @focus="focusedBlock = idx"
                  v-html="block.content"></div>
                <button v-if="editing" class="block-remove" @click="removeBlock(idx)">&times;</button>
              </div>

              <div v-if="block.type === 'image'" class="block block-image" :class="{ editing }">
                <figure>
                  <img :src="block.src" :alt="block.title" />
                  <figcaption v-if="!editing">{{ block.title }}</figcaption>
                  <input v-else class="image-title-input" :value="block.title"
                    @input="block.title = $event.target.value" placeholder="Enter image title..." />
                </figure>
                <button v-if="editing" class="block-remove" @click="removeBlock(idx)">&times;</button>
              </div>
            </div>

            <div v-if="editing && blocks.length" class="block-divider">
              <button class="add-block-btn" @click.stop="showBlockMenu = showBlockMenu === 'end' ? null : 'end'">+</button>
              <div v-if="showBlockMenu === 'end'" class="block-menu">
                <button @click="addBlock(blocks.length - 1, 'header')">Header</button>
                <button @click="addBlock(blocks.length - 1, 'text')">Text</button>
                <button @click="pickImage()">Image</button>
              </div>
            </div>

            <div v-if="editing && !blocks.length" class="slide-empty-blocks">
              <button class="add-first-block" @click="addBlock(-1, 'text')">Start writing...</button>
              <button class="add-first-block image-btn" @click="pickImage()">Add image</button>
            </div>

            <div v-if="!editing && !blocks.length" class="slide-empty">No description</div>
          </div>

          <div class="slide-links" v-if="task.urls && task.urls.length">
            <h4>Links</h4>
            <a v-for="url in task.urls" :key="url" :href="url" target="_blank">
              <i class="bi bi-link-45deg"></i> {{ url }}
            </a>
          </div>

          <div class="slide-links" v-if="task.files && task.files.length">
            <h4>Files</h4>
            <a v-for="file in task.files" :key="file.name" :href="file.data" :download="file.name" class="file-link">
              <i class="bi bi-file-earmark-arrow-down"></i> {{ file.name }}
            </a>
          </div>
        </div>

        <div v-else class="slide-empty">Task not found</div>
      </div>

      <div class="title-prompt-overlay" v-if="titlePrompt.visible" @click.self="titlePrompt.visible = false">
        <div class="title-prompt-box">
          <h4>Image title / caption</h4>
          <input v-model="titlePrompt.title" placeholder="Enter a title for this image..." @keyup.enter="confirmImageTitle" autofocus />
          <div class="title-prompt-actions">
            <button class="btn-cancel" @click="titlePrompt.visible = false">Skip</button>
            <button class="btn-submit" @click="confirmImageTitle">Add image</button>
          </div>
        </div>
      </div>
    </div>
  `,
});
