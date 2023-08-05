(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
const { getCollapsedCategory } = require('./storage.js')

class DataManager {
    setManager(data) {
        const collapsedCategories = [...getCollapsedCategory(data.collapsed)]
        const dataBlob = { ...data, tests: Object.values(data.tests).flat().map((test, index) => ({
            ...test,
            id: `test_${index}`,
            collapsed: collapsedCategories.includes(test.result.toLowerCase()),
        })) }
        this.data = { ...dataBlob }
        this.renderData = { ...dataBlob }
    }

    get allData() {
        return { ...this.data }
    }
    resetRender() {
        this.renderData = { ...this.data }
    }
    setRender(data) {
        this.renderData.tests = [...data]
    }
    toggleCollapsedItem(id) {
        this.renderData.tests = this.renderData.tests.map((test) =>
            test.id === id ? { ...test, collapsed: !test.collapsed } : test,
        )
    }
    set allCollapsed(collapsed) {
        this.renderData = { ...this.renderData, tests: [...this.renderData.tests.map((test) => (
            { ...test, collapsed }
        ))] }
    }

    get testSubset() {
        return [...this.renderData.tests]
    }
    get allTests() {
        return [...this.data.tests]
    }
    get title() {
        return this.renderData.title
    }
    get environment() {
        return this.renderData.environment
    }
    get collectedItems() {
        return this.renderData.collectedItems
    }
    get isFinished() {
        return this.data.runningState === 'Finished'
    }
}

module.exports = {
    manager: new DataManager(),
}

},{"./storage.js":8}],2:[function(require,module,exports){
const storageModule = require('./storage.js')
const { formatDuration } = require('./utils.js')
const mediaViewer = require('./mediaviewer.js')
const templateEnvRow = document.querySelector('#template_environment_row')
const templateCollGroup = document.querySelector('#template_table-colgroup')
const templateResult = document.querySelector('#template_results-table__tbody')
const aTag = document.querySelector('#template_a')
const listHeader = document.querySelector('#template_results-table__head')
const listHeaderEmpty = document.querySelector('#template_results-table__head--empty')

function htmlToElements(html) {
    const temp = document.createElement('template')
    temp.innerHTML = html
    return temp.content.childNodes
}

const find = (selector, elem) => {
    if (!elem) {
        elem = document
    }
    return elem.querySelector(selector)
}

const findAll = (selector, elem) => {
    if (!elem) {
        elem = document
    }
    return [...elem.querySelectorAll(selector)]
}

const insertAdditionalHTML = (html, element, selector) => {
    Object.keys(html).map((key) => {
        element.querySelectorAll(selector).item(key).insertAdjacentHTML('beforebegin', html[key])
    })
}

const dom = {
    getStaticRow: (key, value) => {
        const envRow = templateEnvRow.content.cloneNode(true)
        const isObj = typeof value === 'object' && value !== null
        const values = isObj ? Object.keys(value).map((k) => `${k}: ${value[k]}`) : null

        const valuesElement = htmlToElements(
            values ? `<ul>${values.map((val) => `<li>${val}</li>`).join('')}<ul>` : `<div>${value}</div>`)[0]
        const td = findAll('td', envRow)
        td[0].textContent = key
        td[1].appendChild(valuesElement)

        return envRow
    },
    getListHeader: ({ resultsTableHeader }) => {
        const header = listHeader.content.cloneNode(true)
        const sortAttr = storageModule.getSort()
        const sortAsc = JSON.parse(storageModule.getSortDirection())

        const regex = /data-column-type="(\w+)/
        const cols = Object.values(resultsTableHeader).reduce((result, value) => {
            if (value.includes("sortable")) {
                const matches = regex.exec(value)
                if (matches) {
                    result.push(matches[1])
                }
            }
            return result
        }, [])
        const sortables = ['result', 'testId', 'duration', ...cols]

        // Add custom html from the pytest_html_results_table_header hook
        insertAdditionalHTML(resultsTableHeader, header, 'th')

        sortables.forEach((sortCol) => {
            if (sortCol === sortAttr) {
                header.querySelector(`[data-column-type="${sortCol}"]`).classList.add(sortAsc ? 'desc' : 'asc')
            }
        })

        return header
    },
    getListHeaderEmpty: () => listHeaderEmpty.content.cloneNode(true),
    getColGroup: () => templateCollGroup.content.cloneNode(true),
    getResultTBody: ({ testId, id, log, duration, extras, resultsTableRow, tableHtml, result, collapsed }) => {
        const resultLower = result.toLowerCase()
        let formattedDuration = formatDuration(duration)
        formattedDuration = formatDuration < 1 ? formattedDuration.ms : formattedDuration.formatted
        const resultBody = templateResult.content.cloneNode(true)
        resultBody.querySelector('tbody').classList.add(resultLower)
        resultBody.querySelector('tbody').id = testId
        resultBody.querySelector('.col-result').innerText = result
        resultBody.querySelector('.col-result').classList.add(`${collapsed ? 'expander' : 'collapser'}`)
        resultBody.querySelector('.col-result').dataset.id = id
        resultBody.querySelector('.col-name').innerText = testId

        resultBody.querySelector('.col-duration').innerText = duration < 1 ? formatDuration(duration).ms : formatDuration(duration).formatted


        if (log) {
            resultBody.querySelector('.log').innerHTML = log
        } else {
            resultBody.querySelector('.log').remove()
        }

        if (collapsed) {
            resultBody.querySelector('.extras-row').classList.add('hidden')
        }

        const media = []
        extras?.forEach(({ name, format_type, content }) => {
            if (['json', 'text', 'url'].includes(format_type)) {
                const extraLink = aTag.content.cloneNode(true)
                const extraLinkItem = extraLink.querySelector('a')

                extraLinkItem.href = content
                extraLinkItem.className = `col-links__extra ${format_type}`
                extraLinkItem.innerText = name
                resultBody.querySelector('.col-links').appendChild(extraLinkItem)
            }

            if (['image', 'video'].includes(format_type)) {
                media.push({ path: content, name, format_type })
            }

            if (format_type === 'html') {
                resultBody.querySelector('.extraHTML').insertAdjacentHTML('beforeend', `<div>${content}</div>`)
            }
        })
        mediaViewer.setUp(resultBody, media)

        // Add custom html from the pytest_html_results_table_row hook
        resultsTableRow && insertAdditionalHTML(resultsTableRow, resultBody, 'td')

        // Add custom html from the pytest_html_results_table_html hook
        tableHtml?.forEach((item) => {
            resultBody.querySelector('td[class="extra"]').insertAdjacentHTML('beforeend', item)
        })

        return resultBody
    },
}

exports.dom = dom
exports.htmlToElements = htmlToElements
exports.find = find
exports.findAll = findAll

},{"./mediaviewer.js":6,"./storage.js":8,"./utils.js":9}],3:[function(require,module,exports){
const { manager } = require('./datamanager.js')
const storageModule = require('./storage.js')

const getFilteredSubSet = (filter) =>
    manager.allData.tests.filter(({ result }) => filter.includes(result.toLowerCase()))

const doInitFilter = () => {
    const currentFilter = storageModule.getVisible()
    const filteredSubset = getFilteredSubSet(currentFilter)
    manager.setRender(filteredSubset)
}

const doFilter = (type, show) => {
    if (show) {
        storageModule.showCategory(type)
    } else {
        storageModule.hideCategory(type)
    }

    const currentFilter = storageModule.getVisible()

    if (currentFilter.length) {
        const filteredSubset = getFilteredSubSet(currentFilter)
        manager.setRender(filteredSubset)
    } else {
        manager.resetRender()
    }
}

module.exports = {
    doFilter,
    doInitFilter,
}

},{"./datamanager.js":1,"./storage.js":8}],4:[function(require,module,exports){
const { redraw, bindEvents } = require('./main.js')
const { doInitFilter } = require('./filter.js')
const { doInitSort } = require('./sort.js')
const { manager } = require('./datamanager.js')
const data = JSON.parse(document.querySelector('#data-container').dataset.jsonblob)

function init() {
    manager.setManager(data)
    doInitFilter()
    doInitSort()
    redraw()
    bindEvents()
}

init()

},{"./datamanager.js":1,"./filter.js":3,"./main.js":5,"./sort.js":7}],5:[function(require,module,exports){
const { formatDuration } = require('./utils.js')
const { dom, findAll } = require('./dom.js')
const { manager } = require('./datamanager.js')
const { doSort } = require('./sort.js')
const { doFilter } = require('./filter.js')
const { getVisible, possibleResults } = require('./storage.js')

const removeChildren = (node) => {
    while (node.firstChild) {
        node.removeChild(node.firstChild)
    }
}

const renderStatic = () => {
    const renderTitle = () => {
        const title = manager.title
        document.querySelector('#title').innerText = title
        document.querySelector('#head-title').innerText = title
    }
    const renderTable = () => {
        const environment = manager.environment
        const rows = Object.keys(environment).map((key) => dom.getStaticRow(key, environment[key]))
        const table = document.querySelector('#environment')
        removeChildren(table)
        rows.forEach((row) => table.appendChild(row))
    }
    renderTitle()
    renderTable()
}

const renderContent = (tests) => {
    const rows = tests.map(dom.getResultTBody)
    const table = document.querySelector('#results-table')
    removeChildren(table)
    const tableHeader = dom.getListHeader(manager.renderData)
    if (!rows.length) {
        tableHeader.appendChild(dom.getListHeaderEmpty())
    }
    table.appendChild(dom.getColGroup())
    table.appendChild(tableHeader)

    rows.forEach((row) => !!row && table.appendChild(row))

    table.querySelectorAll('.extra').forEach((item) => {
        item.colSpan = document.querySelectorAll('th').length
    })
    findAll('.sortable').forEach((elem) => {
        elem.addEventListener('click', (evt) => {
            const { target: element } = evt
            const { columnType } = element.dataset
            doSort(columnType)
            redraw()
        })
    })
    findAll('.col-result').forEach((elem) => {
        elem.addEventListener('click', ({ target }) => {
            manager.toggleCollapsedItem(target.dataset.id)
            redraw()
        })
    })
}

const renderDerived = (tests, collectedItems, isFinished) => {
    const currentFilter = getVisible()
    possibleResults.forEach(({ result, label }) => {
        const count = tests.filter((test) => test.result.toLowerCase() === result).length
        const input = document.querySelector(`input[data-test-result="${result}"]`)
        document.querySelector(`.${result}`).innerText = `${count} ${label}`

        input.disabled = !count
        input.checked = currentFilter.includes(result)
    })

    const numberOfTests = tests.filter(({ result }) =>
        ['Passed', 'Failed', 'XPassed', 'XFailed'].includes(result)).length

    if (isFinished) {
        const accTime = tests.reduce((prev, { duration }) => prev + duration, 0)
        const formattedAccTime = formatDuration(accTime)
        const testWord = numberOfTests > 1 ? 'tests' : 'test'
        const durationText = formattedAccTime.hasOwnProperty('ms') ? formattedAccTime.ms : formattedAccTime.formatted

        document.querySelector('.run-count').innerText = `${numberOfTests} ${testWord} took ${durationText}.`
        document.querySelector('.summary__reload__button').classList.add('hidden')
    } else {
        document.querySelector('.run-count').innerText = `${numberOfTests} / ${collectedItems} tests done`
    }
}

const bindEvents = () => {
    const filterColumn = (evt) => {
        const { target: element } = evt
        const { testResult } = element.dataset

        doFilter(testResult, element.checked)
        redraw()
    }
    findAll('input[name="filter_checkbox"]').forEach((elem) => {
        elem.removeEventListener('click', filterColumn)
        elem.addEventListener('click', filterColumn)
    })
    document.querySelector('#show_all_details').addEventListener('click', () => {
        manager.allCollapsed = false
        redraw()
    })
    document.querySelector('#hide_all_details').addEventListener('click', () => {
        manager.allCollapsed = true
        redraw()
    })
}

const redraw = () => {
    const { testSubset, allTests, collectedItems, isFinished } = manager

    renderStatic()
    renderContent(testSubset)
    renderDerived(allTests, collectedItems, isFinished)
}

exports.redraw = redraw
exports.bindEvents = bindEvents

},{"./datamanager.js":1,"./dom.js":2,"./filter.js":3,"./sort.js":7,"./storage.js":8,"./utils.js":9}],6:[function(require,module,exports){
class MediaViewer {
    constructor(assets) {
        this.assets = assets
        this.index = 0
    }
    nextActive() {
        this.index = this.index === this.assets.length - 1 ? 0 : this.index + 1
        return [this.activeFile, this.index]
    }
    prevActive() {
        this.index = this.index === 0 ? this.assets.length - 1 : this.index -1
        return [this.activeFile, this.index]
    }

    get currentIndex() {
        return this.index
    }
    get activeFile() {
        return this.assets[this.index]
    }
}


const setUp = (resultBody, assets) => {
    if (!assets.length) {
        resultBody.querySelector('.media').classList.add('hidden')
        return
    }

    const mediaViewer = new MediaViewer(assets)
    const leftArrow = resultBody.querySelector('.media-container__nav--left')
    const rightArrow = resultBody.querySelector('.media-container__nav--right')
    const mediaName = resultBody.querySelector('.media__name')
    const counter = resultBody.querySelector('.media__counter')
    const imageEl = resultBody.querySelector('img')
    const sourceEl = resultBody.querySelector('source')
    const videoEl = resultBody.querySelector('video')

    const setImg = (media, index) => {
        if (media?.format_type === 'image') {
            imageEl.src = media.path

            imageEl.classList.remove('hidden')
            videoEl.classList.add('hidden')
        } else if (media?.format_type === 'video') {
            sourceEl.src = media.path

            videoEl.classList.remove('hidden')
            imageEl.classList.add('hidden')
        }

        mediaName.innerText = media?.name
        counter.innerText = `${index + 1} / ${assets.length}`
    }
    setImg(mediaViewer.activeFile, mediaViewer.currentIndex)

    const moveLeft = () => {
        const [media, index] = mediaViewer.prevActive()
        setImg(media, index)
    }
    const doRight = () => {
        const [media, index] = mediaViewer.nextActive()
        setImg(media, index)
    }
    const openImg = () => {
        window.open(mediaViewer.activeFile.path, '_blank')
    }

    leftArrow.addEventListener('click', moveLeft)
    rightArrow.addEventListener('click', doRight)
    imageEl.addEventListener('click', openImg)
}

exports.setUp = setUp

},{}],7:[function(require,module,exports){
const { manager } = require('./datamanager.js')
const storageModule = require('./storage.js')

const genericSort = (list, key, ascending) => {
    const sorted = list.sort((a, b) => a[key] === b[key] ? 0 : a[key] > b[key] ? 1 : -1)

    if (ascending) {
        sorted.reverse()
    }
    return sorted
}

const doInitSort = () => {
    const type = storageModule.getSort()
    const ascending = storageModule.getSortDirection()
    const list = manager.testSubset
    const sortedList = genericSort(list, type, ascending)
    manager.setRender(sortedList)
}

const doSort = (type) => {
    const newSortType = storageModule.getSort() !== type
    const currentAsc = storageModule.getSortDirection()
    const ascending = newSortType ? true : !currentAsc
    storageModule.setSort(type)
    storageModule.setSortDirection(ascending)
    const list = manager.testSubset

    const sortedList = genericSort(list, type, ascending)
    manager.setRender(sortedList)
}

exports.doSort = doSort
exports.doInitSort = doInitSort

},{"./datamanager.js":1,"./storage.js":8}],8:[function(require,module,exports){
const possibleResults = [
    { result: 'passed', label: 'Passed' },
    { result: 'skipped', label: 'Skipped' },
    { result: 'failed', label: 'Failed' },
    { result: 'error', label: 'Errors' },
    { result: 'xfailed', label: 'Unexpected failures' },
    { result: 'xpassed', label: 'Unexpected passes' },
    { result: 'rerun', label: 'Reruns' },
]
const possibleFilters = possibleResults.map((item) => item.result)

const getVisible = () => {
    const url = new URL(window.location.href)
    const settings = new URLSearchParams(url.search).get('visible') || ''
    return settings ?
        [...new Set(settings.split(',').filter((filter) => possibleFilters.includes(filter)))] : possibleFilters
}
const hideCategory = (categoryToHide) => {
    const url = new URL(window.location.href)
    const visibleParams = new URLSearchParams(url.search).get('visible')
    const currentVisible = visibleParams ? visibleParams.split(',') : [...possibleFilters]
    const settings = [...new Set(currentVisible)].filter((f) => f !== categoryToHide).join(',')

    url.searchParams.set('visible', settings)
    history.pushState({}, null, unescape(url.href))
}

const showCategory = (categoryToShow) => {
    if (typeof window === 'undefined') {
        return
    }
    const url = new URL(window.location.href)
    const currentVisible = new URLSearchParams(url.search).get('visible')?.split(',') || [...possibleFilters]
    const settings = [...new Set([categoryToShow, ...currentVisible])]
    const noFilter = possibleFilters.length === settings.length || !settings.length

    noFilter ? url.searchParams.delete('visible') : url.searchParams.set('visible', settings.join(','))
    history.pushState({}, null, unescape(url.href))
}
const setFilter = (currentFilter) => {
    if (!possibleFilters.includes(currentFilter)) {
        return
    }
    const url = new URL(window.location.href)
    const settings = [currentFilter, ...new Set(new URLSearchParams(url.search).get('filter').split(','))]

    url.searchParams.set('filter', settings)
    history.pushState({}, null, unescape(url.href))
}

const getSort = () => {
    const url = new URL(window.location.href)
    return new URLSearchParams(url.search).get('sort') || 'result'
}
const setSort = (type) => {
    const url = new URL(window.location.href)
    url.searchParams.set('sort', type)
    history.pushState({}, null, unescape(url.href))
}

const getCollapsedCategory = (config) => {
    let categories
    if (typeof window !== 'undefined') {
        const url = new URL(window.location.href)
        const collapsedItems = new URLSearchParams(url.search).get('collapsed')
        switch (true) {
            case !config && collapsedItems === null:
                categories = ['passed'];
                break;
            case collapsedItems?.length === 0 || /^["']{2}$/.test(collapsedItems):
                categories = [];
                break;
            case /^all$/.test(collapsedItems) || (collapsedItems === null && /^all$/.test(config)):
                categories = [...possibleFilters];
                break;
            default:
                categories = collapsedItems?.split(',').map(item => item.toLowerCase()) || config;
                break;
        }
    } else {
        categories = []
    }
    return categories
}

const getSortDirection = () => JSON.parse(sessionStorage.getItem('sortAsc'))

const setSortDirection = (ascending) => sessionStorage.setItem('sortAsc', ascending)

module.exports = {
    getVisible,
    setFilter,
    hideCategory,
    showCategory,
    getSort,
    getSortDirection,
    setSort,
    setSortDirection,
    getCollapsedCategory,
    possibleFilters,
    possibleResults,
}

},{}],9:[function(require,module,exports){
const formattedNumber = (number) =>
    number.toLocaleString('en-US', {
        minimumIntegerDigits: 2,
        useGrouping: false,
    })

const formatDuration = ( totalSeconds ) => {
    if (totalSeconds < 1) {
        return {ms: `${Math.round(totalSeconds * 1000)} ms`}
    }

    const hours = Math.floor(totalSeconds / 3600)
    let remainingSeconds = totalSeconds % 3600
    const minutes = Math.floor(remainingSeconds / 60)
    remainingSeconds = remainingSeconds % 60
    const seconds = Math.round(remainingSeconds)

    return {
      seconds: `${Math.round(totalSeconds)} seconds`,
      formatted: `${formattedNumber(hours)}:${formattedNumber(minutes)}:${formattedNumber(seconds)}`,
    }
}

module.exports = { formatDuration }

},{}]},{},[4]);
