<template>
    <div v-if="isDisplayed">
        <div class="panel panel-info">
            <div class="panel-heading cpanel">
                <label for="filter"><img src="../assets/filter.png" alt="Filter" class="img-responsive"></label>
                <select id="filter" class="form-control" v-model="selectedFilter">
                    <option class="option" v-for="filter in filters" :selected="filter =='All'">{{ filter }}</option>
                </select>
                <div class="errors">Errors: <span>{{ errors }}</span></div>
            </div>
            <div class="panel-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <tbody>
                            <tr v-for='segment in filtered'>
                                <td class="number">{{ segment.number }}.</td>
                                <td v-html="segment.original"></td>
                                <td class="warnings"><img src="../assets/warning.png" alt="Warning!" title="It is recommended to use preposition 'та' if a sentence already contains preposition 'й\і!'" v-if="segment.warnings"></td>
                                <td v-html="segment.reviewed"></td>
                                <td class="corrections">{{ segment.corrections }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { eventBus } from '../main'
    export default {
        data() {
            return {
                segments: [],
                selectedFilter: 'All',
                filters: ['All', 'Detected', 'Errors only', 'Correct only', 'Warnings'],
                isDisplayed: false
            }
        },
        created() {
            eventBus.$on('textWasSubmitted', (txt) => {
                this.segments = JSON.parse(text.value);
                this.isDisplayed = true
            });
            eventBus.$on('newDocument', (isCreated) => {
                this.isDisplayed = false
            });
        },
        computed: {
            filtered() {
              if (this.selectedFilter == 'All') {
                  return this.segments
              }
              else if (this.selectedFilter == 'Detected') {
                  return this.segments.filter((element) => {
                      return element.changed;
                  });
              }
              else if (this.selectedFilter == 'Errors only') {
                  return this.segments.filter((element) => {
                      return element.corrections > 0;
                  });
              }
              else if (this.selectedFilter == 'Correct only') {
                  return this.segments.filter((element) => {
                      return (element.changed && element.corrections == 0);
                  });
              }
              else if (this.selectedFilter == 'Warnings') {
                  return this.segments.filter((element) => {
                      return element.warnings;
                  });
              }
            },
            errors() {
                for (var i = 0, corrections = 0; i < this.segments.length; i++) {
                    corrections += this.segments[i].corrections;
                }
                return corrections;
            }
        }
    }
</script>

<style scoped>

    .cpanel {
        display: flex;
        flex-direction: row;
    }

    label, select, .errors {
        display: flex;
        align-items: center;
    }

    label img {
        margin-right:5px;
    }

    select {
        width: 20%;
    }

    .option {
        padding: 5px;
    }

    .errors {
        font-weight: bold;
        font-size: 1.1em;
        margin-left: auto;
    }

    .errors span {
        font-weight: normal;
        margin-left: 5px;
    }

    td {
        padding: 8px;
    }

    .number, .warnings, .corrections {
        text-align: center;
    }
</style>