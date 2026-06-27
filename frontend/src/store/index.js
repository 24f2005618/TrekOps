import {createStore} from 'vuex';

const store = createStore(
    {
        state: {
            user:{
                token: null,
                roles : []
            }
        },
        mutations: {
            setUser(state, value){
                localStorage.setItem("user",JSON.stringify(value));
                state.user = value;
            }
        },
        getters:{
            getUser(state){
                return state.user; 
            }
        }
    }
)

export default store;