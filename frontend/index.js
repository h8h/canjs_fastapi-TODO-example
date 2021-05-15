import {
  realtimeRestModel,
  StacheElement,
  type
} from "can";
import view from "./views/app.stache";
import './styles/main.less';

const Todo = realtimeRestModel("/api/v1/todos/{id}").ObjectType;

class TodosApp extends StacheElement {
  static view = view;

  static props = {
    newName: String,
    selected: type.maybe(Todo),

    get todosPromise() {
      return Todo.getList({ sort: "name" });
    }
  };

  save() {
    const todo = new Todo({ name: this.newName, complete: false });
    todo.save();
    this.newName = "";
  }

  saveTodo(todo) {
    todo.save();
    this.selected = null;
  }
}

customElements.define("todos-app", TodosApp);
