/**
 * Module giving an interactive GUI/text editor for editing YANG Suite replays.
 */
let replay_editor = function() {
    "use strict";

    /**
     * Default configuration
     */
    let config = {
        editorTheme: "cui133",
        editorIcons: "fontawesome50",
    };

    let c = config;

    let state = {
        editor: null,
        editorDialog: null,
        loadedCategoryName: null,
        loadedReplayName: null,
    };

    /* Adapt Bootstrap 4 JSONEditor theme to Cisco UI Kit 1.3.3 */
    JSONEditor.defaults.themes.cui133 = JSONEditor.defaults.themes.bootstrap4.extend({
        getButtonHolder: function() {
            return document.createElement('span');
        },
        getButton: function(text, icon, title) {
            var el = this._super(text, icon, title);
            el.classList.add("btn", "btn--secondary", "btn--small");
            if (!text) {
                el.classList.add("btn--icon");
            }
            return el;
        },
        getFormControl: function(label, input, description) {
            let group;
            if (label && input.type === "checkbox") {
                return this._super(label, input, description);
            } else {
                group = document.createElement("div");
                group.classList.add("form-group", "label--inline");
                let subgroup = document.createElement("div");
                group.appendChild(subgroup);
                subgroup.classList.add("form-group__text");
                if (input.type.includes("select")) {
                    subgroup.classList.add("select");
                }
                if (label) {
                    subgroup.appendChild(label);
                }
                subgroup.appendChild(input);
            }

            if (description) group.appendChild(description);

            return group;
        },
        getHeader: function(text) {
            var el = document.createElement('h5');
            if(typeof text === "string") {
                el.textContent = text;
            } else {
                el.appendChild(text);
            }

            return el;
        },
        getIndentedPanel: function() {
            let el = this._super();
            el.style.paddingRight = "0px";
            el.style.borderRight = "none";
            el.style.paddingBottom = "3px";
            return el;
        },
        getTextareaInput: function() {
            let el = this._super();
            el.rows = 4;
            return el;
        },
    });

    /* Adapt FontAwesome5 JSONEditor theme to our FontAwesome 5.0 library */
    JSONEditor.defaults.iconlibs.fontawesome50 = JSONEditor.AbstractIconLib.extend({
        mapping: {
            collapse: 'caret-down',
            expand: 'caret-right',
            delete: 'times',
            edit: 'pencil-alt',
            add: 'plus',
            cancel: 'ban',
            save: 'save',
            moveup: 'arrow-up',
            movedown: 'arrow-down',
            copy: 'copy',
            clear: 'times-circle',
            time: 'clock',
            calendar: 'calendar'
        },
        icon_prefix: 'fas fa-'
    });

    /**
     * Helper function to initEditorDialog. Create the actual JSONEditor.
     */
    function makeEditor(elementID) {
        let editorElement = document.getElementById(elementID);
        state.editor = new JSONEditor(editorElement, {
            theme: config.editorTheme,
            iconlib: config.editorIcons,
            template: 'default',
            schema: {
                type: 'object',
                title: 'replay',
                headerTemplate: "{{self.name}}",
                required: ['category', 'description', 'name', 'autogenerated', 'segments'],
                options: {
                    disable_properties: true,
                },
                properties: {
                    'name': {
                        type: 'string',
                    },
                    'category': {
                        type: 'string',
                    },
                    'description': {
                        type: 'string',
                        format: "textarea",
                    },
                    'autogenerated': {
                        type: 'boolean',
                    },
                    'images': {
                        type: 'array',
                        format: 'table',
                        items: {
                            type: 'string',
                            title: 'image',
                        },
                        options: {
                            collapsed: true,
                        },
                    },
                    'platforms': {
                        type: 'array',
                        format: 'table',
                        items: {
                            type: 'string',
                            title: 'platform',
                        },
                        options: {
                            collapsed: true,
                        },
                    },
                    'segments': {
                        type: 'array',
                        options: {
                            disable_array_delete_last_row: true,
                        },
                        title: "replay segments",
                        items: {
                            type: 'object',
                            title: "replay segment",
                            headerTemplate: "replay segment {{self.segment}}",
                            required: ['segment', 'yang'],
                            options: {
                                collapsed: true,
                                disable_properties: true,
                            },
                            properties: {
                                'segment': {
                                    type: 'integer',
                                },
                                'description': {
                                    type: 'string',
                                    format: "textarea",
                                },
                                'commit': {
                                    type: 'string',
                                    enum: ['', 'add'],
                                    options: {
                                        enum_titles: ['omit', 'add'],
                                    },
                                },
                                'yang': {
                                    type: 'object',
                                    options: {
                                        disable_collapse: true,
                                        disable_edit_json: true,
                                        remove_empty_properties: true,
                                    },
                                    properties: {
                                        'proto-op': {
                                            type: 'string',
                                            enum: [
                                                'edit-config',
                                                'get-config',
                                                'get',
                                                'action',
                                                'rpc'
                                            ]
                                        },
                                        'rpc': {
                                            type: 'string',
                                            format: 'textarea',
                                        },
                                        'modules': {
                                            type: 'object',
                                            options: {
                                                disable_collapse: true,
                                                disable_edit_json: true,
                                            },
                                            additionalProperties: {
                                                type: 'object',
                                                required: ['configs', 'namespace_prefixes'],
                                                options: {
                                                    collapsed: true,
                                                    disable_properties: true,
                                                },
                                                properties: {
                                                    'revision': {
                                                        type: 'string',
                                                    },
                                                    'namespace_prefixes': {
                                                        type: 'object',
                                                        title: "XML namespace prefixes",
                                                        additionalProperties: {
                                                            type: 'string'
                                                        },
                                                        options: {
                                                            collapsed: true,
                                                            remove_empty_properties: true,
                                                        },
                                                    },
                                                    'configs': {
                                                        type: 'array',
                                                        options: {
                                                            disable_array_delete_last_row: true,
                                                        },
                                                        items: {
                                                            type: 'object',
                                                            title: "config entry",
                                                            required: ['xpath'],
                                                            options: {
                                                                remove_empty_properties: true,
                                                            },
                                                            properties: {
                                                                'xpath': {
                                                                    type: 'string',
                                                                },
                                                                'value': {
                                                                    type: 'string',
                                                                },
                                                                'edit-op': {
                                                                    type: 'string',
                                                                    enum: [
                                                                        'create',
                                                                        'merge',
                                                                        'replace',
                                                                        'delete',
                                                                        'remove',
                                                                    ]
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        });

        return state.editor;
    };

    /**
     * Instantiate the JSONEditor instance as a jqueryui dialog
     *
     * @param {string} elementID - id string of element to use for the dialog
     */
    function initEditorDialog(elementID) {
        let id;
        let sel;
        if (elementID.startsWith("#")) {
            id = elementID.slice(1);
            sel = elementID;
        } else {
            id = elementID;
            sel = "#" + elementID;
        }
        // Create the JSONEditor instance
        let editor = makeEditor(id);
        // Create the containing dialog
        state.editorDialog = $(sel);
        state.editorDialog.dialog({
            width: $(window).width() * 0.95,
            height: $(window).height() * 0.95,
            autoOpen: false,
            modal: true,
            buttons: {
                'Cancel': function() {
                    $(sel).dialog("close");
                },
                'Save Changes': function() {
                    let data = editor.getValue();
                    if (data.category != state.loadedCategoryName ||
                        data.name != state.loadedReplayName) {
                        if (confirm("You've changed the replay name and/or category. " +
                                    "Do you want to delete the old entry " +
                                    "(category \"" + state.loadedCategoryName +
                                    "\", replay \"" + state.loadedReplayName +
                                    "\")?")) {
                            tasks.deleteTask(state.loadedReplayName, state.loadedCategoryName);
                        }
                    }
                    tasks.saveTask(data.name,
                                   data.description,
                                   data.segments,
                                   data.platforms,
                                   data.images,
                                   data.category,
                                   true,  //overwrite existing replay
                                   data.autogenerated,
                                  )
                        .then(function() {
                            $(sel).dialog("close");
                        });
                },
            },
        });

        return state.editorDialog;
    };

    function showEditorDialog(category, replay) {
        tasks.getTask(replay, category, function(retObj) {
            state.editor.setValue(retObj.task);
            state.loadedCategoryName = retObj.task.category;
            state.loadedReplayName = retObj.task.name;
            state.editorDialog.dialog({
                title: retObj.task.name,
                width: $(window).width() * 0.95,
                height: $(window).height() * 0.95,
            }).dialog("open");
        });
    };

    /**
     * Public APIs
     */
    return {
        config: config,
        state: state,
        initEditorDialog: initEditorDialog,
        showEditorDialog: showEditorDialog,
    };
}();
