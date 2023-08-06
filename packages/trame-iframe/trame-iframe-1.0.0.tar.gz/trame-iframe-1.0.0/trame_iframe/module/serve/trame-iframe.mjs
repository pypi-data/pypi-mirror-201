import { ref as f, onMounted as u, onBeforeUnmount as c, inject as p } from "vue";
const l = {
  setup(r, { emit: e, expose: m }) {
    const o = f(null);
    function s(a) {
      o.value && o.value.contentWindow.postMessage(a, "*");
    }
    function t(a) {
      var i, n;
      (i = a == null ? void 0 : a.data) != null && i.emit && e(a.data.emit, (n = a.data) == null ? void 0 : n.value);
    }
    return u(() => {
      o.value.contentWindow.addEventListener("message", t);
    }), c(() => {
      o.value.contentWindow.removeEventListener("message", t);
    }), m({ triggerEmit: t, postMessage: s }), { triggerEmit: t, postMessage: s, elem: o };
  },
  template: '<iframe ref="elem" v-bind="$attrs"></iframe>'
}, g = {
  setup(r, { emit: e }) {
    const m = p("trame");
    function o(t) {
      window.postMessage(t, "*");
    }
    function s(t) {
      var a, i, n;
      (a = t == null ? void 0 : t.data) != null && a.emit && e(t.data.emit, (i = t.data) == null ? void 0 : i.value), (n = t == null ? void 0 : t.data) != null && n.state && m.state.update(t.data.state);
    }
    return u(() => {
      window.addEventListener("message", s);
    }), c(() => {
      window.removeEventListener("message", s);
    }), { postMessage: o, triggerEmit: s };
  }
}, d = {
  IFrame: l,
  Communicator: g
};
function E(r) {
  Object.keys(d).forEach((e) => {
    r.component(e, d[e]);
  });
}
export {
  E as install
};
