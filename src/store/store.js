import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export const store = new Vuex.Store({
    state: {
        text: '',
        selectedComponent: 'text-input'
    },
    getters: {
        getText: state => {
            return state.text;
        },
        getComponent: state => {
            return state.selectedComponent;
        }
    },
    mutations: {
        createNew: state => {
            state.text = '';
            state.selectedComponent = 'text-input';
        },
        check: (state, text) => {
            state.text = text;
            state.selectedComponent = 'result-output'
        }
    },
    actions: {
        createNew: ({ commit }) => {
            commit('createNew');
        },
        check: ({ commit }, text) => {
            commit('check', text);
        }
    }
});