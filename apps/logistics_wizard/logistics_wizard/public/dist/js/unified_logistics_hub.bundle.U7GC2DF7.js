(()=>{var ae=Object.defineProperty,se=Object.defineProperties;var ce=Object.getOwnPropertyDescriptors;var J=Object.getOwnPropertySymbols;var le=Object.prototype.hasOwnProperty,oe=Object.prototype.propertyIsEnumerable;var Y=(p,e,t)=>e in p?ae(p,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):p[e]=t,Z=(p,e)=>{for(var t in e||(e={}))le.call(e,t)&&Y(p,t,e[t]);if(J)for(var t of J(e))oe.call(e,t)&&Y(p,t,e[t]);return p},ee=(p,e)=>se(p,ce(e));window.UNIFIED_LOGISTICS_HUB_HTML=`<div class="logistics-page-container">
    <!-- LEFT VERTICAL SIDEBAR TAB NAVIGATION (Hidden - replaced by top horizontal tab bar to remove redundancy with Frappe system sidebar) -->
    <aside class="logistics-tabs-nav" id="logistics-sidebar-nav" style="display: none !important;">
    </aside>

    <!-- RIGHT MAIN CONTENT AREA (Takes 100% full width) -->
    <div class="logistics-main-content" style="width: 100%; flex: 1;">
        <!-- TOP HORIZONTAL TAB BAR (Sleek Modern SaaS Style) -->
        <!-- HORIZONTAL TAB BAR REMOVED -->
        <!-- TAB 1: EXECUTIVE DASHBOARD (GLOBAL OPERATIONS COMMAND CENTER) -->
        <div class="logistics-tab-pane" id="tab-pane-executive">
            <!-- Header bar with filter and refresh -->
            <div class="exec-header-bar">
                <div class="exec-title-block">
                    <h2 class="exec-title">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="3" width="7" height="9"></rect>
                            <rect x="14" y="3" width="7" height="5"></rect>
                            <rect x="14" y="12" width="7" height="9"></rect>
                            <rect x="3" y="16" width="7" height="5"></rect>
                        </svg>
                        Executive Logistics Command Center
                    </h2>
                    
                </div>
                <div class="exec-header-actions">
                    <div class="exec-filter-group">
                        <label for="exec-time-range" class="exec-filter-label"><i class="fa fa-calendar"></i> Chu k\u1EF3:</label>
                        <select id="exec-time-range" class="form-control exec-time-select">
                            <option value="30d" selected>30 ng\xE0y g\u1EA7n \u0111\xE2y</option>
                            <option value="90d">Qu\xFD hi\u1EC7n t\u1EA1i (Q4)</option>
                            <option value="ytd">N\u0103m 2026</option>
                        </select>
                    </div>
                    <button class="btn btn-default btn-sm" id="exec-btn-refresh" title="L\xE0m m\u1EDBi s\u1ED1 li\u1EC7u">
                        <i class="fa fa-refresh"></i> L\xE0m m\u1EDBi
                    </button>
                </div>
            </div>

            <!-- SECTION 1: 4 VISUAL METRIC TILES C\xD3 MINI PROGRESS BAR -->
            <div class="exec-kpi-grid">
                <!-- KPI 1: Active Cases -->
                <div class="exec-kpi-card">
                    <div class="exec-kpi-top">
                        <div class="exec-kpi-info">
                            <span class="exec-kpi-label">T\u1ED5ng \u0110\u01A1n H\xE0ng \u0110ang Ch\u1EA1y</span>
                            <div class="exec-kpi-val-row">
                                <span class="exec-kpi-value" id="exec-val-total-cases">--</span>
                                <span class="exec-badge exec-badge-success" id="exec-badge-growth">Live</span>
                            </div>
                        </div>
                        <div class="exec-kpi-icon-wrap icon-blue">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
                        </div>
                    </div>
                    <div class="exec-kpi-progress">
                        <div class="exec-progress-bar bg-blue" id="exec-bar-import" style="width: 71%;" title="Nh\u1EADp kh\u1EA9u: 20"></div>
                        <div class="exec-progress-bar bg-emerald" id="exec-bar-export" style="width: 29%;" title="Xu\u1EA5t kh\u1EA9u: 8"></div>
                    </div>
                    <div class="exec-kpi-footer">
                        <span><i class="fa fa-arrow-circle-down text-blue"></i> Nh\u1EADp kh\u1EA9u: <strong id="exec-sub-import">20</strong> (71%)</span>
                        <span><i class="fa fa-arrow-circle-up text-emerald"></i> Xu\u1EA5t kh\u1EA9u: <strong id="exec-sub-export">8</strong> (29%)</span>
                    </div>
                </div>

                <!-- KPI 2: In-Transit Shipments -->
                <div class="exec-kpi-card">
                    <div class="exec-kpi-top">
                        <div class="exec-kpi-info">
                            <span class="exec-kpi-label">L\xF4 H\xE0ng \u0110ang Di Chuy\u1EC3n</span>
                            <div class="exec-kpi-val-row">
                                <span class="exec-kpi-value" id="exec-val-in-transit">18</span>
                                <span class="exec-badge exec-badge-info">64% Lu\u1ED3ng h\xE0ng</span>
                            </div>
                        </div>
                        <div class="exec-kpi-icon-wrap icon-cyan">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>
                        </div>
                    </div>
                    <div class="exec-kpi-progress">
                        <div class="exec-progress-bar bg-cyan" id="exec-bar-transit" style="width: 78%;"></div>
                    </div>
                    <div class="exec-kpi-footer">
                        <span><i class="fa fa-ship text-cyan"></i> 14 \u0110\u01B0\u1EDDng bi\u1EC3n</span>
                        <span><i class="fa fa-plane text-blue"></i> 4 H\xE0ng kh\xF4ng</span>
                    </div>
                </div>

                <!-- KPI 3: Actionable Alerts -->
                <div class="exec-kpi-card">
                    <div class="exec-kpi-top">
                        <div class="exec-kpi-info">
                            <span class="exec-kpi-label">C\u1EA3nh B\xE1o & R\u1EE7i Ro Ch\u1EADm Tr\u1EC5</span>
                            <div class="exec-kpi-val-row">
                                <span class="exec-kpi-value text-amber" id="exec-val-alerts">3</span>
                                <span class="exec-badge exec-badge-amber">C\u1EA7n ch\xFA \xFD</span>
                            </div>
                        </div>
                        <div class="exec-kpi-icon-wrap icon-amber">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                        </div>
                    </div>
                    <div class="exec-kpi-progress">
                        <div class="exec-progress-bar bg-amber" style="width: 10%;"></div>
                    </div>
                    <div class="exec-kpi-footer">
                        <span><i class="fa fa-exclamation-triangle text-amber"></i> 1 Tr\u1EC5 l\u1ECBch ETA</span>
                        <span><i class="fa fa-clock-o text-amber"></i> 2 H\u1EA1n h\u1EA3i quan</span>
                    </div>
                </div>

                <!-- KPI 4: Total Spend & Budget -->
                <div class="exec-kpi-card">
                    <div class="exec-kpi-top">
                        <div class="exec-kpi-info">
                            <span class="exec-kpi-label">T\u1ED5ng Chi Ph\xED & Ng\xE2n S\xE1ch</span>
                            <div class="exec-kpi-val-row">
                                <span class="exec-kpi-value text-emerald" id="exec-val-spend">$1,245,500</span>
                                <span class="exec-badge exec-badge-success">-2.7% Ti\u1EBFt ki\u1EC7m</span>
                            </div>
                        </div>
                        <div class="exec-kpi-icon-wrap icon-emerald">
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                        </div>
                    </div>
                    <div class="exec-kpi-progress">
                        <div class="exec-progress-bar bg-emerald" style="width: 97.3%;"></div>
                    </div>
                    <div class="exec-kpi-footer">
                        <span>D\u1EF1 to\xE1n: <strong>$1,280,000</strong></span>
                        <span>Ch\xEAnh l\u1EC7ch: <strong class="text-emerald">-$34,500</strong></span>
                    </div>
                </div>
            </div>

            <!-- SECTION 2: END-TO-END OPERATIONAL PIPELINE FUNNEL -->
            <div class="exec-pipeline-section">
                <div class="exec-section-header">
                    <div class="exec-section-title-wrap">
                        <h3 class="exec-section-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
                            D\xF2ng Ch\u1EA3y H\xE0ng H\xF3a To\xE0n H\u1EC7 Th\u1ED1ng (End-to-End Pipeline Funnel)
                        </h3>
                        
                    </div>
                </div>
                <div class="exec-pipeline-flow" id="exec-pipeline-container">
                    <!-- Populated dynamically via JS -->
                </div>
            </div>

            <!-- SECTION 3: 2-COLUMN GRID (RADAR S\u1EE8C KH\u1ECEE + C\u01A0 C\u1EA4U CHI PH\xCD) -->
            <div class="exec-grid-two-col">
                <!-- LEFT: OPERATIONAL HEALTH & MODALITY -->
                <div class="exec-card">
                    <div class="exec-card-header">
                        <h4 class="exec-card-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"></path></svg>
                            S\u1EE9c Kh\u1ECFe V\u1EADn H\xE0nh & Ph\u01B0\u01A1ng Th\u1EE9c V\u1EADn Chuy\u1EC3n
                        </h4>
                    </div>
                    <div class="exec-card-body">
                        <div class="exec-health-wrap">
                            <!-- SVG Donut Chart -->
                            <div class="exec-donut-box">
                                <svg class="exec-donut-svg" viewBox="0 0 36 36">
                                    <path class="donut-ring" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#f1f5f9" stroke-width="3.8"/>
                                    <path class="donut-segment segment-ontime" id="donut-segment-ontime" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#10b981" stroke-width="3.8" stroke-dasharray="81, 100" stroke-dashoffset="0"/>
                                    <path class="donut-segment segment-atrisk" id="donut-segment-atrisk" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#f59e0b" stroke-width="3.8" stroke-dasharray="13, 100" stroke-dashoffset="-81"/>
                                    <path class="donut-segment segment-critical" id="donut-segment-critical" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#ef4444" stroke-width="3.8" stroke-dasharray="6, 100" stroke-dashoffset="-94"/>
                                </svg>
                                <div class="exec-donut-center">
                                    <span class="donut-score" id="exec-health-score">94.2%</span>
                                    <span class="donut-label">\u1ED4n \u0110\u1ECBnh</span>
                                </div>
                            </div>
                            <div class="exec-health-legend" id="exec-health-legend">
                                <div class="legend-item">
                                    <span class="legend-dot bg-emerald"></span>
                                    <span class="legend-text">\u0110\xFAng Ti\u1EBFn \u0110\u1ED9 (On-Time)</span>
                                    <strong class="legend-val" id="legend-ontime-val">26 \u0111\u01A1n (81%)</strong>
                                </div>
                                <div class="legend-item">
                                    <span class="legend-dot bg-amber"></span>
                                    <span class="legend-text">C\u1EA7n Theo D\xF5i (At Risk)</span>
                                    <strong class="legend-val" id="legend-atrisk-val">4 \u0111\u01A1n (13%)</strong>
                                </div>
                                <div class="legend-item">
                                    <span class="legend-dot bg-coral"></span>
                                    <span class="legend-text">S\u1EF1 C\u1ED1 / Ch\u1EADm Tr\u1EC5</span>
                                    <strong class="legend-val" id="legend-critical-val">2 \u0111\u01A1n (6%)</strong>
                                </div>
                            </div>
                        </div>

                        <div class="exec-divider"></div>

                        <!-- Modality Split Progress Bars -->
                        <div class="exec-modality-block">
                            <span class="exec-subhead">T\u1EF7 Tr\u1ECDng Ph\u01B0\u01A1ng Th\u1EE9c V\u1EADn Chuy\u1EC3n:</span>
                            <div class="modality-row">
                                <span class="modality-title"><i class="fa fa-ship text-cyan"></i> \u0110\u01B0\u1EDDng bi\u1EC3n (FCL/LCL)</span>
                                <div class="modality-bar-wrap">
                                    <div class="modality-bar bg-cyan" style="width: 70%;"></div>
                                </div>
                                <span class="modality-pct">70% (22 l\xF4)</span>
                            </div>
                            <div class="modality-row">
                                <span class="modality-title"><i class="fa fa-plane text-blue"></i> H\xE0ng kh\xF4ng (Air Cargo)</span>
                                <div class="modality-bar-wrap">
                                    <div class="modality-bar bg-blue" style="width: 20%;"></div>
                                </div>
                                <span class="modality-pct">20% (6 l\xF4)</span>
                            </div>
                            <div class="modality-row">
                                <span class="modality-title"><i class="fa fa-truck text-emerald"></i> V\u1EADn t\u1EA3i b\u1ED9 (Trucking)</span>
                                <div class="modality-bar-wrap">
                                    <div class="modality-bar bg-emerald" style="width: 10%;"></div>
                                </div>
                                <span class="modality-pct">10% (3 l\xF4)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- RIGHT: FINANCIAL COST BREAKDOWN & BUDGET CONTROL -->
                <div class="exec-card">
                    <div class="exec-card-header">
                        <h4 class="exec-card-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
                            C\u01A1 C\u1EA5u Chi Ph\xED Logistics Theo Nh\xF3m Nghi\u1EC7p V\u1EE5
                        </h4>
                        <span class="exec-badge exec-badge-success">Ti\u1EBFt ki\u1EC7m +$34,500</span>
                    </div>
                    <div class="exec-card-body">
                        <div class="exec-cost-bars-list" id="exec-cost-breakdown-list">
                            <!-- Populated dynamically via JS -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- SECTION 4: 2-COLUMN GRID (H\xC0NH LANG V\u1EACN T\u1EA2I + TH\u1EBA C\u1EA2NH B\xC1O H\xC0NH \u0110\u1ED8NG NHANH) -->
            <div class="exec-grid-two-col">
                <!-- LEFT: KEY TRADE CORRIDORS -->
                <div class="exec-card">
                    <div class="exec-card-header">
                        <h4 class="exec-card-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
                            H\xE0nh Lang V\u1EADn T\u1EA3i Tr\u1ECDng \u0110i\u1EC3m & T\u1EA7n Su\u1EA5t
                        </h4>
                    </div>
                    <div class="exec-card-body" id="exec-corridors-container">
                        <!-- Populated dynamically via JS -->
                    </div>
                </div>

                <!-- RIGHT: ACTIONABLE RADAR ALERTS -->
                <div class="exec-card">
                    <div class="exec-card-header">
                        <h4 class="exec-card-title">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                            S\u1EF1 C\u1ED1 C\u1EA7n Can Thi\u1EC7p Ngay (Action Radar)
                        </h4>
                        <span class="exec-subhead-badge text-amber">3 V\u1EA5n \u0111\u1EC1</span>
                    </div>
                    <div class="exec-card-body" id="exec-alerts-container">
                        <!-- Populated dynamically via JS with action button linking to Tab 2 -->
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: TRADE CASE DOSSIER -->
        <div class="logistics-tab-pane active" id="tab-pane-trade-case">
        <!-- N\xDAT CH\u1ECCN H\u1ED2 S\u01A0 N\u1EB0M NGAY TRONG TAB N\xC0Y -->
        <div class="tc-tab-control-bar">
            <div class="tc-select-case-group">
                <label for="tc-case-selector" class="tc-select-label">
                    <i class="fa fa-folder-open" style="color: #0284c7;"></i> Ch\u1ECDn h\u1ED3 s\u01A1 Trade Case:
                </label>
                <div class="tc-select-wrapper">
                    <select id="tc-case-selector" class="form-control tc-case-select-dropdown">
                        <!-- Populated dynamically via API -->
                    </select>
                </div>
            </div>
            <div class="tc-tab-control-actions">
                <button class="btn btn-default btn-sm" id="tc-btn-refresh-case" title="L\xE0m m\u1EDBi t\u1ED5ng quan">
                    <i class="fa fa-refresh"></i> L\xE0m m\u1EDBi
                </button>
                <button class="btn btn-default btn-sm" id="tc-btn-edit-case" title="Ch\u1EC9nh s\u1EEDa h\u1ED3 s\u01A1 DocType">
                    <i class="fa fa-pencil"></i> Ch\u1EC9nh s\u1EEDa Case
                </button>
            </div>
        </div>

        <!-- KH\u1ED0I 1: HEADER IDENTIFICATION -->
        <div class="tc-card" id="tc-header-card">
            <div class="tc-header-top">
                <div class="tc-id-badges">
                    <span class="tc-badge-id" id="tc-id-text"><span id="tc-header-id">--</span></span>
                    <span class="tc-badge-status" id="tc-status-badge"><span id="tc-header-status">LOADING</span></span>
                    <span class="tc-badge-health warning" id="tc-health-badge"><span id="tc-header-health">Health: --</span></span>
                    <span class="tc-badge-priority" id="tc-priority-badge"><span id="tc-header-priority">Normal Priority</span></span>
                </div>
                <div class="tc-header-actions">
                    <button class="btn btn-xs btn-default" id="tc-btn-refresh" title="L\xE0m m\u1EDBi"><i class="fa fa-refresh"></i> L\xE0m m\u1EDBi</button>
                </div>
            </div>
            <div class="tc-master-grid" id="tc-master-details">
                <div class="tc-detail-col">
                    <div class="tc-detail-label">Lo\u1EA1i h\xECnh / \u0110\u1ED1i t\xE1c:</div>
                    <div class="tc-detail-val" id="tc-party-text"><span id="tc-meta-party">Import Case \u2014 ABC Electronics Co., Ltd</span></div>
                </div>
                <div class="tc-detail-col">
                    <div class="tc-detail-label">\u0110\u01A1n mua h\xE0ng (PO/SO):</div>
                    <div class="tc-detail-val" id="tc-docref-text"><span id="tc-meta-po">--</span></div>
                </div>
                <div class="tc-detail-col">
                    <div class="tc-detail-label">Ph\u01B0\u01A1ng th\u1EE9c & Incoterm:</div>
                    <div class="tc-detail-val" id="tc-mode-incoterm"><span id="tc-meta-mode-incoterm">Ocean \u2022 FOB</span></div>
                </div>
                <div class="tc-detail-col">
                    <div class="tc-detail-label">Tuy\u1EBFn \u0111\u01B0\u1EDDng (Origin \u2794 Dest):</div>
                    <div class="tc-detail-val" id="tc-route-text"><span id="tc-meta-route">Shanghai Port, China \u2794 Da Nang Port, Vietnam</span></div>
                </div>
                <div class="tc-detail-col">
                    <div class="tc-detail-label">Ng\u01B0\u1EDDi ph\u1EE5 tr\xE1ch ch\xEDnh:</div>
                    <div class="tc-detail-val" id="tc-owner-text"><span id="tc-meta-owner">Nguyen Van A (Logistics)</span></div>
                </div>
                <div class="tc-detail-col">
                    <div class="tc-detail-label">Th\u1EDDi h\u1EA1n d\u1EF1 ki\u1EBFn \u0111\xF3ng:</div>
                    <div class="tc-detail-val" id="tc-expected-close"><span id="tc-meta-expected-close">2026-10-15</span></div>
                </div>
            </div>
        </div>

        <!-- KH\u1ED0I 2: LIFECYCLE STEPPER -->
        <div class="tc-card" id="tc-lifecycle-card">
            <div class="tc-card-header">
                <div class="tc-card-title">
                    <i class="fa fa-map-signs" style="color: #0284c7;"></i> Ti\u1EBFn Tr\xECnh Nghi\u1EC7p V\u1EE5 To\xE0n V\xF2ng \u0110\u1EDDi (Trade Case Lifecycle)
                </div>
                <div class="tc-current-stage-callout" id="tc-current-stage-callout">
                    <span id="tc-lifecycle-current-label">Giai \u0111o\u1EA1n hi\u1EC7n t\u1EA1i: <strong>In Transit</strong></span>
                </div>
            </div>
            <div class="tc-lifecycle-stepper" id="tc-lifecycle-stepper">
                <!-- Rendered dynamically via JS -->
            </div>
            <div class="tc-milestone-subgrid">
                <div class="tc-milestone-box prev">
                    <div class="tc-ms-tag">M\u1ED0C V\u1EEAA QUA (PREVIOUS)</div>
                    <div class="tc-ms-title" id="tc-prev-ms-title"><span id="tc-ms-prev-title">Vessel Departed Shanghai Port</span></div>
                    <div class="tc-ms-date" id="tc-prev-ms-date"><span id="tc-ms-prev-date">01/10/2026</span></div>
                </div>
                <div class="tc-milestone-box next">
                    <div class="tc-ms-tag">M\u1ED0C K\u1EBE TI\u1EBEP (NEXT)</div>
                    <div class="tc-ms-title" id="tc-next-ms-title"><span id="tc-ms-next-title">Arrival Da Nang Port</span></div>
                    <div class="tc-ms-date" id="tc-next-ms-date"><span id="tc-ms-next-date">08/10/2026 (Tr\u1EC5 +2 ng\xE0y)</span></div>
                </div>
            </div>
        </div>

        <!-- KH\u1ED0I 3: OVERALL HEALTH & READINESS GRID -->
        <div class="tc-health-grid" id="tc-health-grid">
            <!-- 6 th\u1EBB tr\u1EA1ng th\xE1i Rendered dynamically via JS -->
        </div>

        <!-- KH\u1ED0I 4 & 5: SHIPMENT SUMMARY & DOCUMENT READINESS -->
        <div class="tc-two-col-grid">
            <!-- KH\u1ED0I 4: SHIPMENT SUMMARY -->
            <div class="tc-card" id="tc-shipment-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-ship" style="color: #0284c7;"></i> V\u1EADn \u0110\u01A1n & H\xE0nh Tr\xECnh (Shipment Summary)
                    </div>
                    <button class="btn btn-xs btn-primary font-weight-bold tc-btn-goto-shipment tc-drill-down-shipment" id="tc-btn-goto-shipment" name="tc-btn-goto-shipment">
                        Xem Shipment Tracking <i class="fa fa-arrow-right"></i>
                    </button>
                </div>
                <div class="tc-shipment-summary-content" id="tc-shipment-body">
                    <div id="tc-shipment-summary-body"></div>
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>

            <!-- KH\u1ED0I 5: DOCUMENT READINESS -->
            <div class="tc-card" id="tc-documents-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-file-text-o" style="color: #0284c7;"></i> H\u1ED3 S\u01A1 & Ch\u1EE9ng T\u1EEB (Document Readiness)
                    </div>
                    <span class="tc-badge-soft" id="tc-docs-pct-badge"><span id="tc-doc-readiness-badge">8 / 10 S\u1EB5n s\xE0ng (80%)</span></span>
                </div>
                <div class="tc-docs-content" id="tc-docs-body"><div id="tc-doc-readiness-body"></div>
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>
        </div>

        <!-- KH\u1ED0I 6 & 7: CUSTOMS & LANDED COST -->
        <div class="tc-two-col-grid">
            <!-- KH\u1ED0I 6: CUSTOMS & COMPLIANCE -->
            <div class="tc-card" id="tc-customs-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-gavel" style="color: #0284c7;"></i> H\u1EA3i Quan & Tu\xE2n Th\u1EE7 (Customs & Compliance)
                    </div>
                    <span class="tc-badge-soft" id="tc-customs-status-badge"><span id="tc-customs-badge">PREPARING (70%)</span></span>
                </div>
                <div class="tc-customs-content" id="tc-customs-body">
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>

            <!-- KH\u1ED0I 7: COST SUMMARY (LANDED COST) -->
            <div class="tc-card" id="tc-cost-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-calculator" style="color: #0284c7;"></i> Chi Ph\xED & Gi\xE1 Th\xE0nh Nh\u1EADp Kh\u1EA9u (Landed Cost Summary)
                    </div>
                    <span class="tc-badge-soft" id="tc-cost-status-badge">IN PROGRESS (+7.9%)</span>
                </div>
                <div class="tc-cost-content" id="tc-cost-body">
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>
        </div>

        <!-- KH\u1ED0I 8 & 9: WAREHOUSE & OPEN EXCEPTIONS -->
        <div class="tc-two-col-grid">
            <!-- KH\u1ED0I 8: WAREHOUSE READINESS -->
            <div class="tc-card" id="tc-warehouse-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-building-o" style="color: #0284c7;"></i> Kho H\xE0ng & Giao Nh\u1EADn (Warehouse Readiness)
                    </div>
                    <span class="tc-badge-soft" id="tc-warehouse-status-badge"><span id="tc-wh-badge">NOT READY</span></span>
                </div>
                <div class="tc-warehouse-content" id="tc-warehouse-body"><div id="tc-wh-body"></div>
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>

            <!-- KH\u1ED0I 9: OPEN EXCEPTIONS -->
            <div class="tc-card" id="tc-exceptions-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-exclamation-triangle" style="color: #d97706;"></i> S\u1EF1 C\u1ED1 & Ngo\u1EA1i L\u1EC7 \u0110ang M\u1EDF (Top Open Exceptions)
                    </div>
                    <span class="tc-badge-soft danger" id="tc-open-exceptions-badge"><span id="tc-exceptions-badge">3 Open (1 Qu\xE1 h\u1EA1n)</span></span>
                </div>
                <div class="tc-exceptions-content" id="tc-exceptions-body"><div id="tc-exceptions-body-inner"></div>
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>
        </div>

        <!-- KH\u1ED0I 10 & 11: UPCOMING ACTIONS & ERP DOCUMENTS -->
        <div class="tc-two-col-grid">
            <!-- KH\u1ED0I 10: UPCOMING ACTIONS & DEADLINES -->
            <div class="tc-card" id="tc-actions-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-calendar-check-o" style="color: #0284c7;"></i> H\xE0nh \u0110\u1ED9ng Ti\u1EBFp Theo & H\u1EA1n \u0110\u1ECBnh (Upcoming Actions)
                    </div>
                    <span class="tc-subtitle-tag">B\xE2y gi\u1EDD c\u1EA7n l\xE0m g\xEC ti\u1EBFp theo?</span>
                </div>
                <div class="tc-actions-content" id="tc-actions-body">
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>

            <!-- KH\u1ED0I 11: RELATED ERP DOCUMENTS -->
            <div class="tc-card" id="tc-erp-docs-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-link" style="color: #0284c7;"></i> Ch\u1EE9ng T\u1EEB ERPNext Li\xEAn K\u1EBFt (Related ERP Documents)
                    </div>
                </div>
                <div class="tc-erp-docs-content" id="tc-related-erp-body">
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>
        </div>

        <!-- KH\u1ED0I 12 & 13: RESPONSIBILITY MATRIX & ACTIVITY TIMELINE -->
        <div class="tc-two-col-grid">
            <!-- KH\u1ED0I 12: RESPONSIBILITY MATRIX -->
            <div class="tc-card" id="tc-responsibility-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-users" style="color: #0284c7;"></i> Ph\xE2n C\xF4ng Tr\xE1ch Nhi\u1EC7m (Responsibility Matrix)
                    </div>
                </div>
                <div class="tc-responsibility-content" id="tc-responsibility-body">
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>

            <!-- KH\u1ED0I 13: ACTIVITY TIMELINE -->
            <div class="tc-card" id="tc-timeline-card">
                <div class="tc-card-header">
                    <div class="tc-card-title">
                        <i class="fa fa-history" style="color: #0284c7;"></i> Nh\u1EADt K\xFD Ho\u1EA1t \u0110\u1ED9ng & L\u1ECBch S\u1EED (Activity Audit Timeline)
                    </div>
                </div>
                <div class="tc-timeline-content" id="tc-activity-body">
                    <!-- Rendered dynamically via JS -->
                </div>
            </div>
        </div>

        <!-- KH\u1ED0I 14: QUICK ACTIONS & STAGE GATE -->
        <div class="tc-card" id="tc-stage-gate-card">
            <div class="tc-card-header">
                <div class="tc-card-title">
                    <i class="fa fa-bolt" style="color: #0284c7;"></i> Thao T\xE1c Nhanh & Ch\u1ED1t Ch\u1EB7n H\u1ED3 S\u01A1 (Quick Actions & Stage Gate)
                </div>
            </div>
            <div class="tc-stage-gate-content" id="tc-stage-gate-body">
                <!-- Rendered dynamically via JS -->
            </div>
        </div>
    </div>

    <!-- TAB 2: SHIPMENT TRACKING HUB (100% NGUY\xCAN B\u1EA2N C\u1EE6A 7d1ef41) -->
    <div class="logistics-tab-pane" id="tab-pane-shipment-tracking">
        <div class="shipment-tracking-hub-container">
            <!-- Top Action Header -->
            <div class="hub-header-bar">
                <div class="hub-title-block">
                    <h2 class="hub-title">
                        <span class="hub-title-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0071E3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <polygon points="3 11 22 2 13 21 11 13 3 11"/>
                            </svg>
                        </span>
                        <span class="hub-title-text">Trung T\xE2m Qu\u1EA3n Tr\u1ECB V\u1EADn Chuy\u1EC3n To\xE0n C\u1EA7u</span>
                    </h2>
                    
                </div>
                <div class="hub-header-actions">
                    <button class="btn btn-default btn-sm hub-btn-refresh" id="hub-btn-refresh" title="L\xE0m m\u1EDBi d\u1EEF li\u1EC7u">
                        <i class="fa fa-refresh"></i> L\xE0m m\u1EDBi
                    </button>
                    <button class="btn btn-primary btn-sm hub-btn-sync" id="hub-btn-sync-now" title="\u0110\u1ED3ng b\u1ED9 d\u1EEF li\u1EC7u t\u1EE9c th\xEC t\u1EEB h\xE3ng v\u1EADn t\u1EA3i">
                        <i class="fa fa-cloud-download"></i> \u0110\u1ED3ng b\u1ED9 t\u1EE9c th\xEC (Sync Now)
                    </button>
                </div>
            </div>

            <!-- KH\u1ED0I 1: 4 Th\u1EBB KPI Metrics (Icon Vector SVG Monoline) -->
            <div class="hub-kpi-grid">
                <div class="hub-kpi-card kpi-total" data-filter="all">
                    <div class="kpi-icon-wrap">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0071E3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/>
                            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                            <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                            <line x1="12" y1="22.08" x2="12" y2="12"/>
                        </svg>
                    </div>
                    <div class="kpi-data">
                        <div class="kpi-label">T\u1ED5ng s\u1ED1 l\xF4 h\xE0ng</div>
                        <div class="kpi-value" id="kpi-val-total">0</div>
                        <div class="kpi-desc">T\u1EA5t c\u1EA3 v\u1EADn \u0111\u01A1n trong h\u1EC7 th\u1ED1ng</div>
                    </div>
                </div>
                <div class="hub-kpi-card kpi-transit active" data-filter="In Transit">
                    <div class="kpi-icon-wrap">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0071E3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <polygon points="12 2 19 21 12 17 5 21 12 2"/>
                        </svg>
                    </div>
                    <div class="kpi-data">
                        <div class="kpi-label">\u0110ang v\u1EADn chuy\u1EC3n</div>
                        <div class="kpi-value" id="kpi-val-transit">0</div>
                        <div class="kpi-desc">T\xE0u bi\u1EC3n & m\xE1y bay \u0111ang h\xE0nh tr\xECnh</div>
                    </div>
                </div>
                <div class="hub-kpi-card kpi-delayed" data-filter="Delayed">
                    <div class="kpi-icon-wrap">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                            <line x1="12" y1="9" x2="12" y2="13"/>
                            <line x1="12" y1="17" x2="12.01" y2="17"/>
                        </svg>
                    </div>
                    <div class="kpi-data">
                        <div class="kpi-label">Ch\u1EADm ti\u1EBFn \u0111\u1ED9</div>
                        <div class="kpi-value" id="kpi-val-delayed">0</div>
                        <div class="kpi-desc">H\xE0nh tr\xECnh b\u1ECB l\u1EC7ch ETA > 1 ng\xE0y</div>
                    </div>
                </div>
                <div class="hub-kpi-card kpi-stale" data-filter="Stale">
                    <div class="kpi-icon-wrap">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12 6 12 12 16 14"/>
                        </svg>
                    </div>
                    <div class="kpi-data">
                        <div class="kpi-label">C\u1EA3nh b\xE1o ngo\u1EA1i l\u1EC7</div>
                        <div class="kpi-value" id="kpi-val-stale">0</div>
                        <div class="kpi-desc">Ch\u01B0a c\xF3 t\xEDn hi\u1EC7u m\u1EDBi t\u1EEB carrier</div>
                    </div>
                </div>
            </div>

            <!-- KH\u1ED0I 2: B\u1EA3n \u0111\u1ED3 Gi\xE1m s\xE1t To\xE0n c\u1EA7u T\u01B0\u01A1ng t\xE1c -->
            <div class="hub-map-card">
                <div class="hub-card-header">
                    <div class="card-header-title">
                        <span class="header-icon">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071E3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="12" cy="12" r="10"/>
                                <line x1="2" y1="12" x2="22" y2="12"/>
                                <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                            </svg>
                        </span>
                        <span class="header-text" id="hub-map-title">B\u1EA3n \u0111\u1ED3 Gi\xE1m s\xE1t To\xE0n c\u1EA7u (Fleet Overview)</span>
                    </div>
                    <div class="card-header-controls">
                        <span class="badge badge-info" id="hub-selected-shipment-badge" style="display:none;"></span>
                        <button class="btn btn-xs btn-default" id="hub-map-reset-btn" title="Tr\u1EDF v\u1EC1 g\xF3c nh\xECn to\xE0n c\u1EA7u">
                            <i class="fa fa-globe"></i> To\xE0n c\u1EA3nh
                        </button>
                    </div>
                </div>
                <div class="hub-map-wrapper">
                    <div id="lw-hub-map" class="lw-hub-map-canvas"></div>
                    <div id="hub-map-loading" class="hub-map-loading-overlay" style="display:none;">
                        <div class="spinner-border text-primary" role="status"></div>
                        <span>\u0110ang t\u1EA3i l\u1ED9 tr\xECnh & \u0111\u1ECBnh v\u1ECB ph\u01B0\u01A1ng ti\u1EC7n...</span>
                    </div>
                </div>
            </div>

            <!-- KH\u1ED0I 4: Visual Milestones Timeline Stepper (9 M\u1ED1c DCSA) -->
            <div class="hub-timeline-card" id="hub-stepper-card">
                <div class="hub-card-header">
                    <div class="card-header-title">
                        <span class="header-icon">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071E3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="12" cy="12" r="4"/>
                                <line x1="1.05" y1="12" x2="8" y2="12"/>
                                <line x1="16" y1="12" x2="22.95" y2="12"/>
                            </svg>
                        </span>
                        <span class="header-text">Ti\u1EBFn Tr\xECnh 9 M\u1ED1c S\u1EF1 Ki\u1EC7n Qu\u1ED1c T\u1EBF DCSA (Milestones Stepper)</span>
                    </div>
                    <div class="card-header-actions">
                        <span class="hub-stepper-shipment-name" id="stepper-shipment-name">Ch\u01B0a ch\u1ECDn l\xF4 h\xE0ng</span>
                    </div>
                </div>
                <div class="hub-stepper-container">
                    <div class="hub-stepper-track" id="hub-stepper-track">
                        <!-- S\u1EBD \u0111\u01B0\u1EE3c render \u0111\u1ED9ng qua JS (9 m\u1ED1c: BOOKED, GATE_IN, LOADED, DEPARTED, TRANSSHIPMENT, ARRIVED, DISCHARGED, GATE_OUT, DELIVERED) -->
                    </div>
                </div>
            </div>

            <!-- T\u1EA6NG D\u01AF\u1EDAI: Chia 2 C\u1ED9t (B\u1EA3ng l\xF4 h\xE0ng chi ti\u1EBFt 65% + Trung t\xE2m C\u1EA3nh b\xE1o 35%) -->
            <div class="hub-split-section">
                <!-- KH\u1ED0I 3: B\u1EA3ng Qu\u1EA3n tr\u1ECB L\xF4 h\xE0ng Chi ti\u1EBFt (65%) -->
                <div class="hub-table-panel">
                    <div class="hub-card-header">
                        <div class="card-header-title">
                            <span class="header-icon">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071E3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                    <line x1="8" y1="6" x2="21" y2="6"/>
                                    <line x1="8" y1="12" x2="21" y2="12"/>
                                    <line x1="8" y1="18" x2="21" y2="18"/>
                                    <line x1="3" y1="6" x2="3.01" y2="6"/>
                                    <line x1="3" y1="12" x2="3.01" y2="12"/>
                                    <line x1="3" y1="18" x2="3.01" y2="18"/>
                                </svg>
                            </span>
                            <span class="header-text">Danh S\xE1ch L\xF4 H\xE0ng Qu\u1ED1c T\u1EBF</span>
                        </div>
                        <div class="hub-search-box">
                            <i class="fa fa-search hub-search-icon"></i>
                            <input type="text" id="hub-search-input" class="form-control input-sm" placeholder="T\xECm m\xE3 v\u1EADn \u0111\u01A1n, container, B/L, PO, h\xE3ng t\xE0u...">
                        </div>
                    </div>

                    <!-- Filter Tabs -->
                    <div class="hub-filter-tabs">
                        <button class="hub-tab-btn active" data-tab="all">T\u1EA5t c\u1EA3 (<span id="tab-cnt-all">0</span>)</button>
                        <button class="hub-tab-btn" data-tab="In Transit">\u0110ang v\u1EADn chuy\u1EC3n (<span id="tab-cnt-transit">0</span>)</button>
                        <button class="hub-tab-btn" data-tab="Delayed">Tr\u1EC5 h\u1EA1n (<span id="tab-cnt-delayed">0</span>)</button>
                        <button class="hub-tab-btn" data-tab="Stale">M\u1EA5t t\xEDn hi\u1EC7u (<span id="tab-cnt-stale">0</span>)</button>
                        <button class="hub-tab-btn" data-tab="Delivered">\u0110\xE3 giao h\xE0ng (<span id="tab-cnt-delivered">0</span>)</button>
                    </div>

                    <!-- Shipment Data Table -->
                    <div class="hub-table-wrapper">
                        <table class="table table-hover hub-data-table" id="hub-shipments-table">
                            <thead>
                                <tr>
                                    <th style="width: 22%;">V\u1EADn \u0111\u01A1n / Container</th>
                                    <th style="width: 18%;">H\xE3ng t\xE0u & Ph\u01B0\u01A1ng ti\u1EC7n</th>
                                    <th style="width: 20%;">C\u1EA3ng \u0110i \u2794 \u0110\u1EBFn</th>
                                    <th style="width: 15%;">L\u1ECBch tr\xECnh (ETD / ETA)</th>
                                    <th style="width: 13%;">\u0110\u1ED9 tr\u1EC5</th>
                                    <th style="width: 12%; text-align: center;">Thao t\xE1c</th>
                                </tr>
                            </thead>
                            <tbody id="hub-shipments-tbody">
                                <tr>
                                    <td colspan="6" class="text-center text-muted" style="padding: 30px;">
                                        <i class="fa fa-spinner fa-spin"></i> \u0110ang t\u1EA3i d\u1EEF li\u1EC7u v\u1EADn chuy\u1EC3n...
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- KH\u1ED0I 5: Trung T\xE2m C\u1EA3nh B\xE1o Ngo\u1EA1i L\u1EC7 & Bi\u1EBFn \u0110\u1ED9ng ETA (35%) -->
                <div class="hub-exceptions-panel">
                    <div class="hub-card-header">
                        <div class="card-header-title">
                            <span class="header-icon">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                    <line x1="12" y1="8" x2="12" y2="12"/>
                                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                                </svg>
                            </span>
                            <span class="header-text">Trung T\xE2m Ngo\u1EA1i L\u1EC7 & C\u1EA3nh B\xE1o (Exception Center)</span>
                        </div>
                        <span class="badge badge-warning" id="hub-exception-count-badge">0 s\u1EF1 c\u1ED1</span>
                    </div>
                    <div class="hub-exceptions-list" id="hub-exceptions-list">
                        <!-- S\u1EBD \u0111\u01B0\u1EE3c render \u0111\u1ED9ng qua JS -->
                        <div class="text-center text-muted" style="padding: 35px 15px;">
                            <i class="fa fa-check-circle text-success" style="font-size: 28px; margin-bottom: 8px;"></i>
                            <p style="margin: 0; font-size: 13px;">Kh\xF4ng c\xF3 s\u1EF1 c\u1ED1 ho\u1EB7c c\u1EA3nh b\xE1o ngo\u1EA1i l\u1EC7 \u0111ang m\u1EDF.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 3: TRADE COST & LANDED COST MANAGEMENT DASHBOARD -->
    <div class="logistics-tab-pane" id="tab-pane-trade-cost">
            <!-- 1. Top Control Bar (matching tc-tab-control-bar) -->
            <div class="tc-tab-control-bar">
                <div class="tc-select-case-group">
                    <label for="tcd-case-selector" class="tc-select-label">
                        <i class="fa fa-calculator" style="color: #0284c7;"></i> Ch\u1ECDn h\u1ED3 s\u01A1 Trade Case:
                    </label>
                    <div class="tc-select-wrapper">
                        <select id="tcd-case-selector" class="form-control tc-case-select-dropdown">
                            <!-- Populated dynamically via API -->
                        </select>
                    </div>
                </div>
                <div class="tc-tab-control-actions">
                    <div class="hub-filter-tabs" style="border: 1px solid #e2e8f0; border-radius: 6px; background: #ffffff; padding: 2px;">
                        <button class="hub-tab-btn active tcd-type-btn" data-type="all">T\u1EA5t c\u1EA3</button>
                        <button class="hub-tab-btn tcd-type-btn" data-type="import">Nh\u1EADp kh\u1EA9u (Landed Cost)</button>
                        <button class="hub-tab-btn tcd-type-btn" data-type="export">Xu\u1EA5t kh\u1EA9u (Export Margin)</button>
                    </div>
                    <button class="btn btn-default btn-sm" id="tcd-btn-refresh" title="L\xE0m m\u1EDBi"><i class="fa fa-refresh"></i> L\xE0m m\u1EDBi</button>
                    <button class="btn btn-primary btn-sm hub-btn-sync" id="tcd-btn-new-sheet"><i class="fa fa-plus"></i> L\u1EADp Cost Sheet</button>
                    <button class="btn btn-default btn-sm" id="tcd-btn-sync-lcv" title="\u0110\u1ED3ng b\u1ED9 sang ERPNext Landed Cost Voucher"><i class="fa fa-exchange"></i> \u0110\u1ED3ng b\u1ED9 LCV</button>
                </div>
            </div>

            <!-- 2. KPI Summary Grid (4 Cards matching Hub style) -->
            <div class="hub-kpi-grid">
                <div class="hub-kpi-card kpi-total">
                    <div class="kpi-icon-wrap">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2">
                            <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                            <line x1="12" y1="8" x2="12" y2="16"></line>
                            <line x1="8" y1="12" x2="16" y2="12"></line>
                        </svg>
                    </div>
                    <div class="kpi-data">
                        <div class="kpi-label">Tr\u1ECB gi\xE1 h\xE0ng mua (FOB)</div>
                        <div class="kpi-value" id="tcd-kpi-po-val">$125,000.00</div>
                        <div class="kpi-desc">Tr\u1ECB gi\xE1 tr\xEAn h\u1EE3p \u0111\u1ED3ng ngo\u1EA1i th\u01B0\u01A1ng</div>
                    </div>
                </div>

                <div class="hub-kpi-card kpi-transit">
                    <div class="kpi-icon-wrap">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                            <polyline points="14 2 14 8 20 8"></polyline>
                        </svg>
                    </div>
                    <div class="kpi-data">
                        <div class="kpi-label">Chi ph\xED d\u1EF1 to\xE1n (Estimated)</div>
                        <div class="kpi-value" id="tcd-kpi-est-val" style="color: #0284c7;">$16,800.00</div>
                        <div class="kpi-desc">\u0110\u1ECBnh m\u1EE9c chi ph\xED logistics d\u1EF1 ki\u1EBFn</div>
                    </div>
                </div>

                <div class="hub-kpi-card">
                    <div class="kpi-icon-wrap" style="background-color: #ecfdf5;">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2">
                            <line x1="12" y1="1" x2="12" y2="23"></line>
                            <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
                        </svg>
                    </div>
                    <div class="kpi-data">
                        <div class="kpi-label">Chi ph\xED th\u1EF1c t\u1EBF (Actual)</div>
                        <div class="kpi-value" id="tcd-kpi-act-val" style="color: #059669;">$18,350.00</div>
                        <div class="kpi-desc">T\u1ED5ng chi ph\xED theo h\xF3a \u0111\u01A1n nh\xE0 cung c\u1EA5p</div>
                    </div>
                </div>

                <div class="hub-kpi-card kpi-delayed">
                    <div class="kpi-icon-wrap">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2">
                            <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                            <polyline points="17 6 23 6 23 12"></polyline>
                        </svg>
                    </div>
                    <div class="kpi-data">
                        <div class="kpi-label">Ch\xEAnh l\u1EC7ch chi ph\xED (Variance)</div>
                        <div class="kpi-value" id="tcd-kpi-var-val" style="color: #dc2626;">+$1,550.00 (+9.2%)</div>
                        <div class="kpi-desc">C\u1EA3nh b\xE1o: V\u01B0\u1EE3t d\u1EF1 to\xE1n ban \u0111\u1EA7u</div>
                    </div>
                </div>
            </div>

            <!-- 3. Split Section (65% / 35%) -->
            <div class="hub-split-section">
                <!-- C\u1ED8T TR\xC1I (65%): B\u1EA3ng K\xEA Chi Ti\u1EBFt 11 Kho\u1EA3n Chi Ph\xED & Custom Allocation Engine -->
                <div class="hub-table-panel">
                    <div class="hub-card-header">
                        <div class="card-header-title">
                            <span class="header-icon">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2">
                                    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
                                    <line x1="8" y1="21" x2="16" y2="21"></line>
                                    <line x1="12" y1="17" x2="12" y2="21"></line>
                                </svg>
                            </span>
                            <span class="header-text">B\u1EA3ng K\xEA Chi Ti\u1EBFt 11 Kho\u1EA3n Chi Ph\xED Logistics (Cost Sheet Items)</span>
                        </div>
                        <div class="card-header-controls">
                            <span class="badge-status badge-in-transit" id="tcd-status-badge">\u0110ang \u0110\u1ED1i So\xE1t</span>
                        </div>
                    </div>

                    <div class="hub-table-wrapper" style="max-height: 380px;">
                        <table class="table hub-data-table">
                            <thead>
                                <tr>
                                    <th>Kho\u1EA3n Chi Ph\xED (Cost Type)</th>
                                    <th>Nh\xE0 Cung C\u1EA5p</th>
                                    <th>S\u1ED1 H\xF3a \u0110\u01A1n</th>
                                    <th class="text-right">D\u1EF1 To\xE1n</th>
                                    <th class="text-right">Th\u1EF1c T\u1EBF</th>
                                    <th class="text-right">Ch\xEAnh L\u1EC7ch</th>
                                    <th class="text-center">Tr\u1EA1ng Th\xE1i</th>
                                </tr>
                            </thead>
                            <tbody id="tcd-cost-items-tbody">
                                <!-- Rendered dynamically -->
                            </tbody>
                        </table>
                    </div>

                    <!-- Custom Landed Cost Allocation Engine Card inside Panel -->
                    <div style="border-top: 1px solid #e2e8f0; padding: 16px 18px; background: #ffffff;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                            <div>
                                <h4 style="margin: 0; font-size: 13.5px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 8px;">
                                    <i class="fa fa-sliders" style="color: #0d9488;"></i>
                                    Custom Cost Allocation Engine (Ph\xE2n B\u1ED5 Gi\xE1 V\u1ED1n Landed Cost)
                                </h4>
                                <span style="font-size: 11.5px; color: #64748b;">T\u1EF1 \u0111\u1ED9ng ph\xE2n b\u1ED5 chi ph\xED v\xE0o t\u1EEBng m\u1EB7t h\xE0ng trong Purchase Receipt theo chu\u1EA9n k\u1EBF to\xE1n ERPNext</span>
                            </div>
                            <div style="display: flex; gap: 6px;">
                                <button class="btn btn-xs btn-default tcd-alloc-btn active" data-rule="weight"><i class="fa fa-balance-scale"></i> Tr\u1ECDng l\u01B0\u1EE3ng (Weight)</button>
                                <button class="btn btn-xs btn-default tcd-alloc-btn" data-rule="value"><i class="fa fa-dollar"></i> Tr\u1ECB gi\xE1 (Value)</button>
                                <button class="btn btn-xs btn-default tcd-alloc-btn" data-rule="qty"><i class="fa fa-cubes"></i> S\u1ED1 l\u01B0\u1EE3ng (Qty)</button>
                                <button class="btn btn-xs btn-default tcd-alloc-btn" data-rule="volume"><i class="fa fa-cube"></i> Th\u1EC3 t\xEDch (CBM)</button>
                            </div>
                        </div>

                        <div class="table-responsive" style="max-height: 240px; overflow-y: auto;">
                            <table class="table table-bordered hub-data-table" style="font-size: 12px;">
                                <thead>
                                    <tr style="background: #f8fafc;">
                                        <th>M\xE3 H\xE0ng (Item)</th>
                                        <th>T\xEAn M\u1EB7t H\xE0ng</th>
                                        <th class="text-center">S\u1ED1 L\u01B0\u1EE3ng</th>
                                        <th class="text-right">\u0110\u01A1n Gi\xE1 Mua</th>
                                        <th class="text-right">Ph\xED Ph\xE2n B\u1ED5</th>
                                        <th class="text-right">Gi\xE1 V\u1ED1n Th\u1EF1c T\u1EBF (Landed Cost)</th>
                                        <th class="text-center">% T\u0103ng</th>
                                    </tr>
                                </thead>
                                <tbody id="tcd-allocation-tbody">
                                    <!-- Rendered dynamically -->
                                </tbody>
                            </table>
                        </div>

                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; padding-top: 8px; border-top: 1px dashed #e2e8f0; font-size: 12px; flex-wrap: wrap; gap: 8px;">
                            <span style="color: #059669; font-weight: 600;"><i class="fa fa-check-circle"></i> \u0110\u1ED9 l\u1EC7ch l\xE0m tr\xF2n: 0.00 USD (Kh\u1EDBp 100% chi ph\xED th\u1EF1c t\u1EBF)</span>
                            <button class="btn btn-xs btn-primary hub-btn-sync" id="tcd-btn-apply-lcv"><i class="fa fa-check"></i> C\u1EADp Nh\u1EADt Gi\xE1 V\u1ED1n V\xE0o ERPNext LCV</button>
                        </div>
                    </div>
                </div>

                <!-- C\u1ED8T PH\u1EA2I (35%): Audit, LCV Sync, Export Margin -->
                <div class="hub-exceptions-panel">
                    <!-- 1. Audit & Anomaly Detection -->
                    <div class="hub-card-header">
                        <div class="card-header-title">
                            <span class="header-icon">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2">
                                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                                    <line x1="12" y1="9" x2="12" y2="13"></line>
                                    <line x1="12" y1="17" x2="12.01" y2="17"></line>
                                </svg>
                            </span>
                            <span class="header-text">Ki\u1EC3m To\xE1n & R\u1EE7i Ro Chi Ph\xED (Cost Audit)</span>
                        </div>
                        <span class="badge-status badge-stale" id="tcd-audit-badge">1 L\u01B0u \xFD</span>
                    </div>
                    <div class="hub-exceptions-list" id="tcd-audit-list">
                        <!-- Duplicate Check -->
                        <div class="hub-exception-card" style="border-left: 4px solid #10b981;">
                            <div class="exception-card-header">
                                <span class="exception-title" style="color: #047857;"><i class="fa fa-check"></i> Tr\xF9ng L\u1EB7p H\xF3a \u0110\u01A1n (Duplicate Check)</span>
                                <span class="delay-tag-ontime">H\u1EE3p l\u1EC7</span>
                            </div>
                            <div class="exception-card-body">Kh\xF4ng ph\xE1t hi\u1EC7n h\xF3a \u0111\u01A1n tr\xF9ng l\u1EB7p s\u1ED1 ch\u1EE9ng t\u1EEB ho\u1EB7c nh\xE0 cung c\u1EA5p.</div>
                        </div>

                        <!-- Missing Critical Cost Check -->
                        <div class="hub-exception-card warning">
                            <div class="exception-card-header">
                                <span class="exception-title" style="color: #b45309;"><i class="fa fa-exclamation-triangle"></i> Chi Ph\xED Tr\u1ECDng Y\u1EBFu (Missing Cost Check)</span>
                                <span class="delay-tag-positive">C\u1EA7n r\xE0 so\xE1t</span>
                            </div>
                            <div class="exception-card-body">Ch\u01B0a nh\u1EADn h\xF3a \u0111\u01A1n n\xE2ng h\u1EA1 c\u1EA3ng \u0111\xEDch (Port Handling D/O). C\u1EA7n li\xEAn h\u1EC7 \u0111\u1EA1i l\xFD h\xE3ng t\xE0u tr\u01B0\u1EDBc ng\xE0y 14/10.</div>
                        </div>

                        <!-- Wrong-case Check -->
                        <div class="hub-exception-card" style="border-left: 4px solid #10b981;">
                            <div class="exception-card-header">
                                <span class="exception-title" style="color: #047857;"><i class="fa fa-check"></i> G\xE1n \u0110\xFAng V\u1EE5 Vi\u1EC7c (Association Check)</span>
                                <span class="delay-tag-ontime">Kh\u1EDBp 100%</span>
                            </div>
                            <div class="exception-card-body">T\u1EA5t c\u1EA3 6 h\xF3a \u0111\u01A1n d\u1ECBch v\u1EE5 \u0111\u1EC1u tham chi\u1EBFu ch\xEDnh x\xE1c s\u1ED1 PO-2026-0042 v\xE0 Trade Case IMP-2026-001.</div>
                        </div>
                    </div>

                    <!-- 2. ERPNext Landed Cost Voucher Status Card -->
                    <div style="border-top: 1px solid #e2e8f0; padding: 14px 16px; background: #ffffff;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 12.5px; font-weight: 700; color: #0f172a;"><i class="fa fa-link" style="color: #0284c7;"></i> ERPNext Landed Cost Voucher</span>
                            <span class="tc-badge-erp submitted" id="tcd-lcv-badge">LCV-2026-0004</span>
                        </div>
                        <div style="font-size: 11.5px; color: #64748b; line-height: 1.45; margin-bottom: 10px;">
                            D\u1EEF li\u1EC7u ph\xE2n b\u1ED5 \u0111\u01B0\u1EE3c ghi nh\u1EADn t\u1EF1 \u0111\u1ED9ng v\xE0o ch\u1EE9ng t\u1EEB ti\xEAu chu\u1EA9n c\u1EE7a ERPNext, c\u1EADp nh\u1EADt tr\u1EF1c ti\u1EBFp v\xE0o \u0111\u1ECBnh gi\xE1 t\u1ED3n kho (Inventory Valuation) v\xE0 gi\xE1 v\u1ED1n (COGS).
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <a href="/app/landed-cost-voucher" class="btn btn-default btn-xs" style="flex: 1; text-align: center;"><i class="fa fa-external-link"></i> M\u1EDF LCV ERPNext</a>
                        </div>
                    </div>

                    <!-- 3. Export Profitability Card -->
                    <div id="tcd-export-profitability-box" style="border-top: 1px solid #e2e8f0; padding: 14px 16px; background: #ffffff;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 12.5px; font-weight: 700; color: #0f172a;"><i class="fa fa-bar-chart" style="color: #059669;"></i> Hi\u1EC7u Qu\u1EA3 L\xF4 Xu\u1EA5t Kh\u1EA9u (Export Margin)</span>
                            <span class="delay-tag-ontime">+24.3% Bi\xEAn L\u1EE3i Nhu\u1EADn</span>
                        </div>
                        <table class="table tc-table" style="margin-bottom: 0;">
                            <tr>
                                <td class="label-col">Doanh thu xu\u1EA5t kh\u1EA9u:</td>
                                <td class="val-col text-right">$65,000.00</td>
                            </tr>
                            <tr>
                                <td class="label-col">Gi\xE1 v\u1ED1n h\xE0ng b\xE1n (COGS):</td>
                                <td class="val-col text-right">$45,000.00</td>
                            </tr>
                            <tr>
                                <td class="label-col">Chi ph\xED logistics xu\u1EA5t kh\u1EA9u:</td>
                                <td class="val-col text-right">$4,200.00</td>
                            </tr>
                            <tr style="border-top: 1px solid #e2e8f0; font-weight: 700;">
                                <td class="label-col" style="color: #059669;">L\u1EE3i nhu\u1EADn g\u1ED9p th\u1EF1c t\u1EBF:</td>
                                <td class="val-col text-right" style="color: #059669; font-size: 13.5px;">$15,800.00</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>

                <!-- TAB 4: LOGISTICS AI COPILOT WORKSPACE (MODERN GEMINI/CLAUDE/CHATGPT STYLE) -->
        <div class="logistics-tab-pane" id="tab-pane-ai-copilot">
            <div class="lw-copilot-container">
                <!-- Left: Modern Chat Sessions Sidebar (Collapsible) -->
                <aside class="lw-copilot-sessions-panel">
                    <div class="lw-copilot-sessions-header">
                        <button id="copilot-btn-new-chat" class="lw-btn-new-chat" title="T\u1EA1o cu\u1ED9c h\u1ED9i tho\u1EA1i m\u1EDBi">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="12" y1="5" x2="12" y2="19"></line>
                                <line x1="5" y1="12" x2="19" y2="12"></line>
                            </svg>
                            <span>Cu\u1ED9c h\u1ED9i tho\u1EA1i m\u1EDBi</span>
                        </button>
                    </div>
                    <div class="lw-copilot-search-wrap">
                        <svg class="lw-copilot-search-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                        <input type="text" id="copilot-session-search" class="form-control lw-copilot-search-input" placeholder="T\xECm ki\u1EBFm h\u1ED9i tho\u1EA1i...">
                    </div>
                    <div class="lw-copilot-sessions-list" id="copilot-sessions-list">
                        <div class="lw-session-group-title">G\u1EA7n \u0111\xE2y</div>
                        <div class="lw-session-item active" data-prompt="Ph\xE2n t\xEDch chi ti\u1EBFt nguy\xEAn nh\xE2n sai l\u1EC7ch chi ph\xED th\u1EF1c t\u1EBF so v\u1EDBi ng\xE2n s\xE1ch d\u1EF1 to\xE1n c\u1EE7a h\u1ED3 s\u01A1 IMP-2026-001">
                            <svg class="lw-session-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                            </svg>
                            <div class="lw-session-info">
                                <span class="lw-session-title">Ph\xE2n t\xEDch sai l\u1EC7ch chi ph\xED IMP-2026-001</span>
                                <span class="lw-session-time">10:45 AM</span>
                            </div>
                        </div>
                        <div class="lw-session-item" data-prompt="Cho bi\u1EBFt t\u1ECDa \u0111\u1ED9 AIS hi\u1EC7n t\u1EA1i, v\u1EADn t\u1ED1c h\u1EA3i l\xFD v\xE0 d\u1EF1 b\xE1o th\u1EDDi gian c\u1EADp c\u1EA3ng \u0110\xE0 N\u1EB5ng c\u1EE7a t\xE0u Maersk Mc-Kinney Moller">
                            <svg class="lw-session-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                            </svg>
                            <div class="lw-session-info">
                                <span class="lw-session-title">Tra c\u1EE9u l\u1ECBch t\xE0u Maersk Mc-Kinney</span>
                                <span class="lw-session-time">09:12 AM</span>
                            </div>
                        </div>
                        <div class="lw-session-item" data-prompt="Theo Th\xF4ng t\u01B0 85/2026/TT-BTC, m\xE1y m\xF3c thi\u1EBFt b\u1ECB th\xE1o r\u1EDDi ho\u1EB7c ch\u01B0a l\u1EAFp r\xE1p \u0111\u01B0\u1EE3c ph\xE2n lo\u1EA1i theo quy t\u1EAFc n\xE0o v\xE0 th\u1EE7 t\u1EE5c tr\u1EEB l\xF9i ra sao?">
                            <svg class="lw-session-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                            </svg>
                            <div class="lw-session-info">
                                <span class="lw-session-title">Th\xF4ng t\u01B0 85/2026 m\xE1y m\xF3c th\xE1o r\u1EDDi</span>
                                <span class="lw-session-time">14 Oct</span>
                            </div>
                        </div>
                    </div>
                    <!-- Bottom Knowledge Corpus Badge -->
                    <div class="lw-copilot-sidebar-footer">
                        <a href="/app/rag-knowledge-base#knowledge" class="lw-kb-status-link" title="Xem Kho tri th\u1EE9c RAG">
                            <span class="lw-status-indicator-dot"></span>
                            <span class="lw-status-text" id="copilot-rag-status-text"><strong>RAG Corpus:</strong> \u0110ang k\u1EBFt n\u1ED1i...</span>
                        </a>
                    </div>
                </aside>

                <!-- Right: Modern Chat Conversation Canvas -->
                <main class="lw-copilot-chat-workspace">
                    <!-- Modern Clean Header Bar -->
                    <div class="lw-copilot-chat-header">
                        <div class="lw-copilot-title-group">
                            <div class="lw-copilot-avatar">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                                </svg>
                            </div>
                            <div>
                                <div class="lw-model-badge">
                                    <span class="lw-model-name">Logistics AI Copilot</span>
                                    <span class="lw-model-tag">v2.4 \u2022 Hybrid RAG</span>
                                </div>
                            </div>
                        </div>
                        <div class="lw-copilot-actions">
                            <div class="tc-select-case-group" style="margin: 0; display: flex; align-items: center; gap: 6px;">
                                <span style="font-size: 12px; font-weight: 600; color: #64748b;">H\u1ED3 s\u01A1:</span>
                                <select id="copilot-context-case" class="form-control tc-case-select-dropdown" style="height: 32px; font-size: 12px; min-width: 160px; border-radius: 6px;">
                                    <!-- Populated dynamically via API -->
                                </select>
                            </div>
                            <button class="btn btn-default btn-xs" id="copilot-btn-clear" title="X\xF3a m\xE0n h\xECnh tr\xF2 chuy\u1EC7n" style="border-radius: 6px; padding: 5px 10px;">
                                <i class="fa fa-trash-o"></i> X\xF3a
                            </button>
                        </div>
                    </div>

                    <!-- Messages stream thread -->
                    <div class="lw-copilot-messages-thread" id="copilot-messages-thread">
                        <!-- Welcome hero banner with ChatGPT/Claude style prompt cards -->
                        <div class="lw-copilot-welcome-box">
                            <div class="lw-welcome-hero-badge">
                                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#0284c7" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                                    <path d="M2 17l10 5 10-5"></path>
                                    <path d="M2 12l10 5 10-5"></path>
                                </svg>
                            </div>
                            <h3 class="lw-welcome-title">Tr\u1EE3 L\xFD AI Nghi\u1EC7p V\u1EE5 Logistics & Ngo\u1EA1i Th\u01B0\u01A1ng</h3>
                            <p class="lw-welcome-sub">
                                K\u1EBFt n\u1ED1i d\u1EEF li\u1EC7u th\u1EDDi gian th\u1EF1c t\u1EEB Bi\u1EC3u thu\u1EBF XNK, Th\xF4ng t\u01B0 85/2026/TT-BTC, V\u1EADn \u0111\u01A1n DCSA v\xE0 Ph\xE2n b\u1ED5 Landed Cost ERPNext.
                            </p>
                            <div class="lw-starter-cards-grid">
                                <div class="lw-starter-card" data-prompt="Theo Th\xF4ng t\u01B0 85/2026/TT-BTC, m\xE1y m\xF3c thi\u1EBFt b\u1ECB th\xE1o r\u1EDDi ho\u1EB7c ch\u01B0a l\u1EAFp r\xE1p \u0111\u01B0\u1EE3c ph\xE2n lo\u1EA1i theo quy t\u1EAFc n\xE0o v\xE0 th\u1EE7 t\u1EE5c tr\u1EEB l\xF9i ra sao?">
                                    <div class="lw-card-icon icon-blue">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                                    </div>
                                    <div class="lw-card-title">Th\xF4ng t\u01B0 85/2026/TT-BTC & GIR 2(a)</div>
                                    <div class="lw-card-desc">Quy t\u1EAFc ph\xE2n lo\u1EA1i m\xE1y m\xF3c th\xE1o r\u1EDDi v\xE0 th\u1EE7 t\u1EE5c phi\u1EBFu tr\u1EEB l\xF9i linh ki\u1EC7n.</div>
                                </div>

                                <div class="lw-starter-card" data-prompt="Ph\xE2n t\xEDch chi ti\u1EBFt nguy\xEAn nh\xE2n sai l\u1EC7ch chi ph\xED th\u1EF1c t\u1EBF so v\u1EDBi ng\xE2n s\xE1ch d\u1EF1 to\xE1n c\u1EE7a h\u1ED3 s\u01A1 IMP-2026-001">
                                    <div class="lw-card-icon icon-emerald">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                                    </div>
                                    <div class="lw-card-title">Ph\xE2n t\xEDch sai l\u1EC7ch Landed Cost</div>
                                    <div class="lw-card-desc">Ki\u1EC3m tra ch\xEAnh l\u1EC7ch chi ph\xED th\u1EF1c t\u1EBF vs d\u1EF1 to\xE1n l\xF4 h\xE0ng IMP-2026-001 (+9.2%).</div>
                                </div>

                                <div class="lw-starter-card" data-prompt="Cho bi\u1EBFt t\u1ECDa \u0111\u1ED9 AIS hi\u1EC7n t\u1EA1i, v\u1EADn t\u1ED1c h\u1EA3i l\xFD v\xE0 d\u1EF1 b\xE1o th\u1EDDi gian c\u1EADp c\u1EA3ng \u0110\xE0 N\u1EB5ng c\u1EE7a t\xE0u Maersk Mc-Kinney Moller">
                                    <div class="lw-card-icon icon-cyan">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>
                                    </div>
                                    <div class="lw-card-title">Theo d\xF5i t\xE0u Maersk v\u1EC1 \u0110\xE0 N\u1EB5ng</div>
                                    <div class="lw-card-desc">T\u1ECDa \u0111\u1ED9 AIS th\u1EF1c t\u1EBF, v\u1EADn t\u1ED1c h\u1EA3i l\xFD v\xE0 d\u1EF1 b\xE1o th\u1EDDi gian c\u1EADp c\u1EA3ng Ti\xEAn Sa.</div>
                                </div>

                                <div class="lw-starter-card" data-prompt="Gi\u1EA3i th\xEDch Ch\xFA gi\u1EA3i 4 v\xE0 5 Ph\u1EA7n XVI v\u1EC1 ph\xE2n lo\u1EA1i t\u1ED5 h\u1EE3p thi\u1EBFt b\u1ECB m\xE1y m\xF3c li\xEAn k\u1EBFt ch\u1EE9c n\u0103ng">
                                    <div class="lw-card-icon icon-amber">
                                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
                                    </div>
                                    <div class="lw-card-title">Ch\xFA gi\u1EA3i Ph\u1EA7n XVI & Bi\u1EC3u thu\u1EBF</div>
                                    <div class="lw-card-desc">Ch\xFA gi\u1EA3i 4 & 5 Ph\u1EA7n XVI v\u1EC1 t\u1ED5 h\u1EE3p thi\u1EBFt b\u1ECB v\xE0 quy tr\xECnh tr\u1EEB l\xF9i h\u1EA3i quan.</div>
                                </div>
                            </div>
                        </div>

                        <!-- Chat Messages List -->
                        <div id="copilot-chat-history"></div>
                    </div>

                    <!-- Modern Claude/ChatGPT style bottom floating input box -->
                    <div class="lw-copilot-input-area">
                        <div class="lw-copilot-input-box">
                            <textarea id="copilot-input-textarea" class="lw-copilot-textarea" placeholder="H\u1ECFi AI Copilot v\u1EC1 Th\xF4ng t\u01B0 85, ph\xE2n b\u1ED5 gi\xE1 v\u1ED1n, h\xE0nh tr\xECnh t\xE0u... (Enter g\u1EEDi, Shift+Enter xu\u1ED1ng d\xF2ng)" rows="1"></textarea>
                            <button id="copilot-btn-send" class="lw-copilot-send-btn" title="G\u1EEDi c\xE2u h\u1ECFi" disabled>
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <line x1="12" y1="19" x2="12" y2="5"></line>
                                    <polyline points="5 12 12 5 19 12"></polyline>
                                </svg>
                            </button>
                        </div>
                        <div class="lw-copilot-disclaimer">
                            Logistics AI Copilot v2.4 \u2022 K\u1EBFt n\u1ED1i tr\u1EF1c ti\u1EBFp RAG Knowledge Base & D\u1EEF li\u1EC7u ERPNext.
                        </div>
                    </div>
                </main>
            </div>
        </div>
    </div>
</div>`;var B=class{constructor(e){this.wrapper=e,this.currentTab="executive",this.currentCaseId="",this.executiveDashboard=e?e.executive_dashboard:null,this.trackingHub=e?e.shipment_tracking_hub:null,this.overviewController=e?e.trade_case_overview:null,this.tradeCostDashboard=e?e.trade_cost_dashboard:null,this.aiCopilot=e?e.logistics_ai_copilot:null}switch_tab(e,t){t=t||{},this.currentTab=e;let n=this.wrapper?$(this.wrapper):$(document),i="executive";e==="overview"||e==="trade-case"||e==="dossier"?i="overview":e==="tracking"||e==="shipment-tracking-hub"?i="tracking":e==="cost"||e==="trade-cost"||e==="trade-cost-dashboard"?i="cost":e==="copilot"||e==="ai-copilot"||e==="logistics-ai-chatbot"?i="copilot":(e==="executive"||e==="exec"||e==="command-center")&&(i="executive"),n.find(".logistics-nav-tab").removeClass("active"),i==="executive"?n.find("#btn-tab-executive").addClass("active"):i==="overview"?n.find("#btn-tab-overview").addClass("active"):i==="tracking"?n.find("#btn-tab-tracking").addClass("active"):i==="cost"?n.find("#btn-tab-cost").addClass("active"):i==="copilot"&&n.find("#btn-tab-copilot").addClass("active"),n.find(".logistics-tab-pane").removeClass("active").removeAttr("style");let s="#tab-pane-executive";i==="overview"?s="#tab-pane-trade-case":i==="tracking"?s="#tab-pane-shipment-tracking":i==="cost"?s="#tab-pane-trade-cost":i==="copilot"&&(s="#tab-pane-ai-copilot"),i==="copilot"||typeof frappe!="undefined"&&frappe.get_route&&(frappe.get_route()[1]==="logistics-ai-copilot"||frappe.get_route()[1]==="logistics_ai_copilot")?($("#logistics-ai-fab-container").hide(),$("#logistics-ai-drawer").hide()):$("#logistics-ai-fab-container").show();let l=n.find(s);if(l.length&&(l[0].offsetWidth,l.addClass("active")),this.wrapper&&this.wrapper.shipment_tracking_hub&&this.wrapper.shipment_tracking_hub.page){let c={executive:__("Executive Logistics Command Center"),overview:__("Trade Case Dossier"),tracking:__("Shipment Tracking Hub"),cost:__("Trade Cost & Landed Cost Dashboard"),copilot:__("Logistics AI Copilot")};this.wrapper.shipment_tracking_hub.page.set_title(c[i]||c.executive)}if(i==="executive")this.executiveDashboard&&this.executiveDashboard.load_data();else if(i==="tracking")this.trackingHub&&(this.trackingHub&&this.trackingHub.map&&setTimeout(()=>{this.trackingHub.map.invalidateSize()},150),t.shipment_id?this.trackingHub.data?(this.trackingHub.select_shipment(t.shipment_id),this.trackingHub.refresh(t.shipment_id)):this.trackingHub.refresh(t.shipment_id):this.trackingHub.data||this.trackingHub.refresh());else if(i==="overview")this.overviewController&&(t.case_id?this.overviewController.load_case(t.case_id):this.overviewController.currentData||this.overviewController.load_case(this.currentCaseId||""));else if(i==="cost"){if(this.tradeCostDashboard){let c=t.case_id||this.currentCaseId||"";this.tradeCostDashboard.load_data(c)}}else i==="copilot"&&this.aiCopilot&&this.aiCopilot.on_tab_shown(t)}};function q(p){if(!!p)try{let e=$(p);e.addClass("logistics-full-bleed-page");let t=e.closest(".page-container");t.length&&(t.addClass("logistics-full-width"),t.css({"max-width":"100%",padding:"0",margin:"0",width:"100%","background-color":"#f8fafc"}),t.find(".page-head").hide(),t.find(".page-body, .page-content, .layout-main-section-wrapper, .layout-main-section, .layout-main, .container-fluid, .container").css({"max-width":"100%",width:"100%",padding:"0",margin:"0",border:"none","box-shadow":"none",background:"#f8fafc","background-color":"#f8fafc"})),e.find(".page-content.container").removeClass("container").addClass("container-fluid"),e.find(".container").removeClass("container").addClass("container-fluid"),e.find(".page-head").hide(),e.find(".page-body, .page-content, .container-fluid, .layout-main-section-wrapper, .layout-main-section, .layout-main").css({"max-width":"100%",width:"100%",padding:"0",margin:"0",border:"none","box-shadow":"none",background:"#f8fafc","background-color":"#f8fafc"})}catch(e){console.warn("make_page_full_bleed warning:",e)}}function Q(p,e,t){!t||(q(t),t.unifiedHub||(t.executive_dashboard=new X(t),t.shipment_tracking_hub=new F(t,p),t.trade_case_overview=new V(t,t.shipment_tracking_hub),t.trade_cost_dashboard=new K(t),t.logistics_ai_copilot=new G(t),t.unifiedHub=new B(t),t.unifiedHub.executiveDashboard=t.executive_dashboard,t.unifiedHub.trackingHub=t.shipment_tracking_hub,t.unifiedHub.overviewController=t.trade_case_overview,t.unifiedHub.tradeCostDashboard=t.trade_cost_dashboard,t.unifiedHub.aiCopilot=t.logistics_ai_copilot,t.executive_dashboard.unifiedHub=t.unifiedHub,t.trade_case_overview.unifiedHub=t.unifiedHub,t.trade_cost_dashboard.unifiedHub=t.unifiedHub,t.logistics_ai_copilot.unifiedHub=t.unifiedHub,t.switch_to_tab=function(n,i){typeof i=="string"?n==="shipment-tracking-hub"||n==="tracking"?t.unifiedHub.switch_tab("tracking",{shipment_id:i}):n==="cost"||n==="trade-cost"||n==="trade-cost-dashboard"?t.unifiedHub.switch_tab("cost",{case_id:i}):n==="copilot"||n==="ai-copilot"?t.unifiedHub.switch_tab("copilot"):n==="executive"||n==="exec"?t.unifiedHub.switch_tab("executive"):t.unifiedHub.switch_tab("overview",{case_id:i}):t.unifiedHub.switch_tab(n,i)},de(t),t.executive_dashboard.init(),t.trade_case_overview.init(),t.trade_cost_dashboard.init(),t.logistics_ai_copilot.init(),typeof window!="undefined"&&window.initLogisticsAIWidget&&window.initLogisticsAIWidget(),q(t)),U(t,e))}function U(p,e){if(!p||!p.unifiedHub)return;q(p);let t=null,n=null,i=e||"overview";frappe.route_options&&(frappe.route_options.shipment&&(t=frappe.route_options.shipment,i="tracking"),frappe.route_options.case_id&&(n=frappe.route_options.case_id,frappe.route_options.tab||(i="overview")),frappe.route_options.tab&&(i=frappe.route_options.tab),frappe.route_options=null),t&&p.switch_to_tab?p.switch_to_tab("tracking",t):n&&p.switch_to_tab?p.switch_to_tab(i,n):p.switch_to_tab&&p.switch_to_tab(i)}function te(p,e){typeof frappe!="undefined"&&frappe.pages&&frappe.pages[p]&&(frappe.pages[p].on_page_load=function(t){Q(p,e,t)},frappe.pages[p].on_page_show=function(t){U(t,e)})}var X=class{constructor(e){this.wrapper=e,this.data=null,this.currentTimeRange="30d",this.bind_events()}bind_events(){let e=this;$(document).off("click","#exec-btn-refresh").on("click","#exec-btn-refresh",function(t){t.preventDefault(),e.load_data()}),$(document).off("change","#exec-time-range").on("change","#exec-time-range",function(){e.currentTimeRange=$(this).val(),e.load_data()}),$(document).off("click",".exec-action-btn").on("click",".exec-action-btn",function(t){t.preventDefault();let n=$(this).data("case");typeof frappe!="undefined"&&frappe.set_route?(frappe.route_options={case_id:n,tab:"overview"},frappe.set_route("trade-case-overview")):n&&e.wrapper&&e.wrapper.unifiedHub&&e.wrapper.unifiedHub.switch_tab("overview",{case_id:n})}),$(document).off("click",".pipeline-step").on("click",".pipeline-step",function(t){t.preventDefault();let n=$(this).find(".pipeline-step-name").text();frappe&&frappe.show_alert&&frappe.show_alert({message:__("\u0110ang quan s\xE1t ch\u1EB7ng: ")+n,indicator:"blue"},3)})}init(){this.load_data()}load_data(){let e=this;frappe.call({method:"logistics_wizard.api.get_executive_dashboard_summary",args:{time_range:e.currentTimeRange},callback:function(t){t&&t.message&&t.message.status==="success"?(e.data=t.message.data,e.render()):t&&t.message&&t.message.metrics&&(e.data=t.message,e.render())}})}render(){var t,n,i,a,s,l,c,d,o,r,h,v,f,y,C,S,A;if(!this.data)return;let e=this.data;if(e.metrics){let g=e.metrics,u=Number((t=g.total_cases)!=null?t:0),b=Number((n=g.import_cases)!=null?n:0),m=Number((i=g.export_cases)!=null?i:0),T=u>0?Math.round(b/u*100):0,E=u>0?100-T:0;$("#exec-val-total-cases").text(u),$("#exec-bar-import").css("width",T+"%").attr("title",`Nh\u1EADp kh\u1EA9u: ${b}`),$("#exec-bar-export").css("width",E+"%").attr("title",`Xu\u1EA5t kh\u1EA9u: ${m}`);let _=$("#tab-pane-executive .exec-kpi-card");if(_.length>=4){_.eq(0).find(".exec-badge").text(`${Number((a=g.active_cases)!=null?a:u)} \u0111ang x\u1EED l\xFD`),_.eq(0).find(".exec-kpi-footer").html(`<span><i class="fa fa-arrow-circle-down text-blue"></i> Nh\u1EADp kh\u1EA9u: <strong id="exec-sub-import">${b}</strong> (${T}%)</span><span><i class="fa fa-arrow-circle-up text-emerald"></i> Xu\u1EA5t kh\u1EA9u: <strong id="exec-sub-export">${m}</strong> (${E}%)</span>`);let x=Number((s=g.in_transit_shipments)!=null?s:0),L=u>0?Math.min(100,Math.round(x/u*100)):0,I=e.modality_split||{},M=Number((l=I.sea&&I.sea.count)!=null?l:0),w=Number((c=I.air&&I.air.count)!=null?c:0);$("#exec-val-in-transit").text(x),$("#exec-bar-transit").css("width",L+"%"),_.eq(1).find(".exec-badge").text(`${L}% Lu\u1ED3ng h\xE0ng`),_.eq(1).find(".exec-kpi-footer").html(`<span><i class="fa fa-ship text-cyan"></i> ${M} \u0110\u01B0\u1EDDng bi\u1EC3n</span><span><i class="fa fa-plane text-blue"></i> ${w} H\xE0ng kh\xF4ng</span>`);let k=Number((d=g.active_exceptions)!=null?d:0),D=Number((o=g.delayed_shipments)!=null?o:0),H=Number((r=g.customs_stuck)!=null?r:0),O=u>0?Math.min(100,Math.round(k/Math.max(u,1)*100)):0;$("#exec-val-alerts").text(k),_.eq(2).find(".exec-progress-bar").css("width",O+"%"),_.eq(2).find(".exec-badge").text(k>0?"C\u1EA7n ch\xFA \xFD":"\u1ED4n \u0111\u1ECBnh"),_.eq(2).find(".exec-kpi-footer").html(`<span><i class="fa fa-exclamation-triangle text-amber"></i> ${D} Tr\u1EC5 l\u1ECBch ETA</span><span><i class="fa fa-clock-o text-amber"></i> ${H} H\u1EA1n h\u1EA3i quan</span>`);let R=Number((h=g.total_spend)!=null?h:0),P=Number((f=(v=g.total_estimated_spend)!=null?v:e.cost_breakdown&&e.cost_breakdown.total_estimated)!=null?f:0),N=R-P,j=P>0?Math.round(N/P*1e3)/10:0,z=N>0,ie=N>0?"+":"-",W=j>0?"+":"",ne=P>0?Math.min(100,Math.round(R/P*100)):0;$("#exec-val-spend").text("$"+R.toLocaleString("en-US")),_.eq(3).find(".exec-badge").attr("class","exec-badge "+(z?"exec-badge-amber":"exec-badge-success")).text(z?`${W}${j}% V\u01B0\u1EE3t d\u1EF1 to\xE1n`:`${W}${j}% Ti\u1EBFt ki\u1EC7m`),_.eq(3).find(".exec-progress-bar").attr("class","exec-progress-bar "+(z?"bg-amber":"bg-emerald")).css("width",ne+"%"),_.eq(3).find(".exec-kpi-footer").html(`<span>D\u1EF1 to\xE1n: <strong>$${P.toLocaleString("en-US")}</strong></span><span>Ch\xEAnh l\u1EC7ch: <strong class="${z?"text-amber":"text-emerald"}">${N===0?"$0":ie+"$"+Math.abs(N).toLocaleString("en-US")}</strong></span>`)}else $("#exec-sub-import").text(b),$("#exec-sub-export").text(m),$("#exec-val-in-transit").text((y=g.in_transit_shipments)!=null?y:0),$("#exec-val-alerts").text((C=g.active_exceptions)!=null?C:0),$("#exec-val-spend").text("$"+Number((S=g.total_spend)!=null?S:0).toLocaleString("en-US"))}if(e.modality_split){let g=e.modality_split,b=[{key:"sea",icon:"fa-ship text-cyan",label:"\u0110\u01B0\u1EDDng bi\u1EC3n (FCL/LCL)",bar:"bg-cyan"},{key:"air",icon:"fa-plane text-blue",label:"H\xE0ng kh\xF4ng (Air Cargo)",bar:"bg-blue"},{key:"road",icon:"fa-truck text-emerald",label:"V\u1EADn t\u1EA3i b\u1ED9 (Trucking)",bar:"bg-emerald"}].map(T=>{let E=g[T.key]||{pct:0,count:0};return`
                    <div class="modality-row">
                        <span class="modality-title"><i class="fa ${T.icon}"></i> ${T.label}</span>
                        <div class="modality-bar-wrap">
                            <div class="modality-bar ${T.bar}" style="width: ${Number(E.pct||0)}%;"></div>
                        </div>
                        <span class="modality-pct">${Number(E.pct||0)}% (${Number(E.count||0)} l\xF4)</span>
                    </div>
                `}).join(""),m=$("#tab-pane-executive .exec-modality-block");m.length&&m.html('<span class="exec-subhead">T\u1EF7 Tr\u1ECDng Ph\u01B0\u01A1ng Th\u1EE9c V\u1EADn Chuy\u1EC3n:</span>'+b)}if(e.pipeline&&e.pipeline.length>0){let g=e.pipeline.map(u=>`
                    <div class="pipeline-step ${u.status==="warning"?"step-warning":""}" data-step="${u.key}">
                        <div class="pipeline-step-header">
                            <span class="pipeline-step-num">${u.step_no}</span>
                            <span class="pipeline-step-count">${u.count} \u0111\u01A1n</span>
                        </div>
                        <div class="pipeline-step-name">${u.label}</div>
                        <span class="pipeline-step-sub">${u.sub_label}</span>
                        <div class="pipeline-step-bar">
                            <div class="pipeline-step-fill ${u.status==="warning"?"bg-amber":"bg-blue"}" style="width: ${u.pct}%;"></div>
                        </div>
                    </div>
                `).join("");$("#exec-pipeline-container").html(g)}if(e.health_donut){let g=e.health_donut;$("#exec-health-score").text(g.score_pct+"%");let u=g.segments||[],b=0;u.forEach(m=>{m.key==="on_time"?($("#donut-segment-ontime").attr("stroke-dasharray",`${m.pct}, 100`).attr("stroke-dashoffset",b),$("#legend-ontime-val").text(`${m.count} \u0111\u01A1n (${m.pct}%)`)):m.key==="at_risk"?($("#donut-segment-atrisk").attr("stroke-dasharray",`${m.pct}, 100`).attr("stroke-dashoffset",-b),$("#legend-atrisk-val").text(`${m.count} \u0111\u01A1n (${m.pct}%)`)):m.key==="critical"&&($("#donut-segment-critical").attr("stroke-dasharray",`${m.pct}, 100`).attr("stroke-dashoffset",-b),$("#legend-critical-val").text(`${m.count} \u0111\u01A1n (${m.pct}%)`)),b+=m.pct})}if(e.cost_breakdown){let g=e.cost_breakdown,u=$("#exec-cost-breakdown-list").closest(".exec-card").find(".exec-card-header .exec-badge");if(u.length){let b=Number((A=g.savings_amount)!=null?A:(g.total_estimated||0)-(g.total_actual||0)),m=b<0;u.attr("class","exec-badge "+(m?"exec-badge-amber":"exec-badge-success")).text(m?`V\u01B0\u1EE3t +$${Math.abs(b).toLocaleString("en-US")}`:`Ti\u1EBFt ki\u1EC7m +$${b.toLocaleString("en-US")}`)}}if(e.cost_breakdown&&e.cost_breakdown.categories){let g=e.cost_breakdown.categories.map(u=>{let b=u.variance_pct>0?"+":"",m=u.variance_pct<=0?"bg-emerald":"bg-amber";return`
                    <div class="cost-bar-item">
                        <div class="cost-bar-header">
                            <span class="cost-bar-name">${u.name}</span>
                            <div class="cost-bar-figures">
                                <span class="cost-bar-amount">$${Number(u.amount).toLocaleString()}</span>
                                <span class="exec-badge ${u.variance_pct<=0?"exec-badge-success":"exec-badge-amber"}">${b}${u.variance_pct}%</span>
                            </div>
                        </div>
                        <div class="cost-bar-progress">
                            <div class="cost-bar-fill ${m}" style="width: ${u.pct_of_total}%;"></div>
                        </div>
                    </div>
                `}).join("");$("#exec-cost-breakdown-list").html(g)}if(e.corridors&&e.corridors.length>0){let g=e.corridors.map(u=>{let b=u.mode==="Air"?"fa-plane":"fa-ship",m=u.health_level==="warning"?"exec-badge-amber":"exec-badge-success";return`
                    <div class="corridor-item">
                        <div class="corridor-main">
                            <div class="corridor-mode-icon">
                                <i class="fa ${b}"></i>
                            </div>
                            <div>
                                <span class="corridor-name">${u.route}</span>
                                <span class="corridor-meta">${u.active_voyages} chuy\u1EBFn \u0111ang ch\u1EA1y \u2022 Th\u1EDDi gian: ${u.avg_transit}</span>
                            </div>
                        </div>
                        <div class="corridor-status">
                            <span class="exec-badge ${m}">${u.status}</span>
                        </div>
                    </div>
                `}).join("");$("#exec-corridors-container").html(g)}if(e.action_alerts&&e.action_alerts.length>0){let g=e.action_alerts.map(u=>{let b=u.severity==="critical",m=b?"alert-critical":"alert-warning",T=b?"text-coral":"text-amber",E=b?"fa-exclamation-circle":"fa-exclamation-triangle",_=b?"btn-primary":"btn-default";return`
                    <div class="exec-alert-card ${m}">
                        <div class="exec-alert-top">
                            <span class="exec-alert-title">
                                <i class="fa ${E} ${T}"></i>
                                ${u.title}
                            </span>
                            <span class="exec-badge ${b?"exec-badge-amber":"exec-badge-info"}">${u.badge_label}</span>
                        </div>
                        <p class="exec-alert-desc">${u.description}</p>
                        <div class="exec-alert-footer">
                            <span class="exec-alert-tags">H\u1ED3 s\u01A1: <strong>${u.case_id}</strong> (${u.shipment_id})</span>
                            <button class="btn btn-xs ${_} exec-action-btn" data-case="${u.case_id}">
                                ${u.action_text} &rarr;
                            </button>
                        </div>
                    </div>
                `}).join("");$("#exec-alerts-container").html(g)}}};function de(p){(p&&p.shipment_tracking_hub&&p.shipment_tracking_hub.page?$(p.shipment_tracking_hub.page.body):$(document)).off("click",".logistics-nav-tab").on("click",".logistics-nav-tab",function(t){t.preventDefault();let n=$(this).data("tab"),i=$(this).attr("data-route")||$(this).data("route");if(i){let a=typeof frappe!="undefined"&&frappe.get_route_str?frappe.get_route_str():"";if(a!==i&&a!=="logistics-wizard/"+i){frappe.set_route(i);return}}if(n==="rag-admin"||n==="rag-admin-center"){typeof frappe!="undefined"&&frappe.set_route?frappe.set_route("rag-admin-center"):window.location.href="/app/rag-admin-center";return}n&&p.unifiedHub&&p.unifiedHub.switch_tab(n)})}var V=class{constructor(e,t){this.wrapper=e,this.trackingHub=t,this.currentCaseId="",this.availableCases=[],this.currentData=null,this.bind_events()}init(){let e=this;frappe.call({method:"logistics_wizard.api.get_trade_case_list",callback:function(t){if(t&&t.message&&t.message.length>0){e.availableCases=t.message;let n=t.message.map(a=>`<option value="${a.case_id}">${a.label||a.case_id+" - "+a.party}</option>`).join("");$("#tc-case-selector").html(n),e.currentCaseId&&t.message.some(a=>a.case_id===e.currentCaseId)||(e.currentCaseId=t.message[0].case_id),$("#tc-case-selector").val(e.currentCaseId),e.load_case(e.currentCaseId)}else e.load_case(e.currentCaseId||"")}})}bind_events(){let e=this;$(document).on("change","#tc-case-selector",function(){let t=$(this).val();t&&e.load_case(t)}),$(document).on("click","#tc-btn-refresh-case",function(){$(this).find("i").addClass("fa-spin"),e.load_case(e.currentCaseId),setTimeout(()=>{$("#tc-btn-refresh-case").find("i").removeClass("fa-spin")},600)}),$(document).on("click","#tc-btn-refresh",function(){$(this).find("i").addClass("fa-spin"),e.load_case(e.currentCaseId),setTimeout(()=>{$("#tc-btn-refresh").find("i").removeClass("fa-spin")},600)}),$(document).on("click","#tc-btn-edit-case",function(){e.currentData&&e.currentData.case_id&&frappe.set_route("Form","Trade Case",e.currentData.case_id)}),$(document).on("click","#tc-btn-goto-shipment, #tc-drill-down-shipment",function(){let t=null;e.currentData&&e.currentData.shipment_summary&&(t=e.currentData.shipment_summary.shipment_id),typeof frappe!="undefined"&&frappe.set_route?(frappe.route_options={shipment:t,tab:"tracking"},frappe.set_route("shipment-tracking-hub")):e.unifiedHub?e.unifiedHub.switch_tab("tracking",{shipment_id:t}):e.wrapper&&e.wrapper.switch_to_tab&&e.wrapper.switch_to_tab("shipment-tracking-hub",t)}),$(document).on("click","#tc-btn-close-case",function(){e.attempt_close_case()}),$(document).on("click","#btn-upload-doc",function(){let t=e.currentData&&e.currentData.case_id||e.currentCaseId;frappe.prompt([{fieldname:"document_code",fieldtype:"Select",label:"Lo\u1EA1i ch\u1EE9ng t\u1EEB (Document Code)",options:`DOC-CI
DOC-PL
DOC-BL
DOC-AWB
DOC-CO
DOC-INS
DOC-DO
DOC-CUS-IMP
DOC-CUS-EXP
DOC-LIC`,default:"DOC-CO",reqd:1},{fieldname:"file_url",fieldtype:"Attach",label:"T\u1EC7p \u0111\xEDnh k\xE8m (File)",reqd:1},{fieldname:"document_number",fieldtype:"Data",label:"S\u1ED1 ch\u1EE9ng t\u1EEB"},{fieldname:"expiry_date",fieldtype:"Date",label:"Ng\xE0y h\u1EBFt h\u1EA1n (n\u1EBFu c\xF3)"},{fieldname:"change_notes",fieldtype:"Data",label:"Ghi ch\xFA phi\xEAn b\u1EA3n",default:"Uploaded from Trade Case Overview"}],function(n){frappe.call({method:"logistics_wizard.document_engine.api.upload_trade_document_version",args:{case_id:t,document_code:n.document_code,file_url:n.file_url,document_number:n.document_number,expiry_date:n.expiry_date,change_notes:n.change_notes},callback:function(i){let a=i.message||{};a.success?(frappe.show_alert({message:__(`\u0110\xE3 t\u1EA3i l\xEAn ${a.document_code} (v${a.current_version}) \u2014 Tr\u1EA1ng th\xE1i: ${a.status}`),indicator:"green"}),e.load_case(t)):frappe.msgprint({title:__("L\u1ED7i t\u1EA3i ch\u1EE9ng t\u1EEB"),message:a.error||"Kh\xF4ng th\u1EC3 l\u01B0u ch\u1EE9ng t\u1EEB.",indicator:"red"})}})},__("T\u1EA3i l\xEAn Ch\u1EE9ng t\u1EEB Xu\u1EA5t Nh\u1EADp Kh\u1EA9u"),__("L\u01B0u ch\u1EE9ng t\u1EEB"))}),$(document).on("click","#btn-update-customs",function(){let t=e.currentData&&e.currentData.case_id||e.currentCaseId,n=e.currentData&&e.currentData.customs_readiness&&e.currentData.customs_readiness.declaration_name||"";if(!n){frappe.prompt([{fieldname:"customs_office_code",fieldtype:"Data",label:"M\xE3 Chi c\u1EE5c H\u1EA3i quan (VD: 02CI, 03CC)",default:"02CI"},{fieldname:"co_form",fieldtype:"Select",label:"M\u1EABu C/O \u01B0u \u0111\xE3i",options:`None
Form E (ACFTA)
Form D (ATIGA)
EUR.1 (EVFTA)
CPTPP
Form B (Non-Preferential)`,default:"None"},{fieldname:"item_name",fieldtype:"Data",label:"T\xEAn m\u1EB7t h\xE0ng ch\xEDnh",reqd:1},{fieldname:"qty",fieldtype:"Float",label:"S\u1ED1 l\u01B0\u1EE3ng",default:1,reqd:1},{fieldname:"unit_price",fieldtype:"Currency",label:"\u0110\u01A1n gi\xE1 khai b\xE1o",default:100,reqd:1},{fieldname:"suggested_hs_code",fieldtype:"Data",label:"M\xE3 HS \u0111\u1EC1 xu\u1EA5t (8 ch\u1EEF s\u1ED1)"}],function(i){frappe.call({method:"logistics_wizard.customs_engine.api.create_customs_declaration",args:{case_id:t,customs_office_code:i.customs_office_code,co_form:i.co_form,items:JSON.stringify([{item_name:i.item_name,qty:i.qty,unit_price:i.unit_price,suggested_hs_code:i.suggested_hs_code||"",hs_approval_status:i.suggested_hs_code?"Proposed":"Pending",vat_rate:10}])},callback:function(a){let s=a.message||{};s.success?(frappe.show_alert({message:__(`\u0110\xE3 l\u1EADp t\u1EDD khai H\u1EA3i quan ${s.name}`),indicator:"green"}),e.load_case(t)):frappe.msgprint({title:__("L\u1ED7i l\u1EADp t\u1EDD khai"),message:s.error||"Kh\xF4ng th\u1EC3 t\u1EA1o t\u1EDD khai.",indicator:"red"})}})},__("Kh\u1EDFi t\u1EA1o T\u1EDD khai H\u1EA3i quan"),__("T\u1EA1o t\u1EDD khai"));return}frappe.prompt([{fieldname:"action_mode",fieldtype:"Select",label:"Nghi\u1EC7p v\u1EE5 H\u1EA3i quan c\u1EA7n th\u1EF1c hi\u1EC7n",options:`C\u1EADp nh\u1EADt tr\u1EA1ng th\xE1i t\u1EDD khai
G\u1EE3i \xFD m\xE3 HS b\u1EB1ng AI/RAG
Ph\xEA duy\u1EC7t / T\u1EEB ch\u1ED1i HS (Chuy\xEAn vi\xEAn)`,default:"C\u1EADp nh\u1EADt tr\u1EA1ng th\xE1i t\u1EDD khai",reqd:1},{fieldname:"target_status",fieldtype:"Select",label:"Chuy\u1EC3n tr\u1EA1ng th\xE1i quy tr\xECnh",options:`Ready
Declared
Processing
Cleared
Rejected
Preparing`,default:"Ready",depends_on:'eval:doc.action_mode=="C\u1EADp nh\u1EADt tr\u1EA1ng th\xE1i t\u1EDD khai"'},{fieldname:"declaration_no",fieldtype:"Data",label:"S\u1ED1 t\u1EDD khai VNACCS/VCIS",default:e.currentData.customs_readiness&&e.currentData.customs_readiness.declaration_no||"",depends_on:'eval:doc.action_mode=="C\u1EADp nh\u1EADt tr\u1EA1ng th\xE1i t\u1EDD khai"'},{fieldname:"customs_lane",fieldtype:"Select",label:"Ph\xE2n lu\u1ED3ng H\u1EA3i quan",options:`Not Declared
Green
Yellow
Red`,default:e.currentData.customs_readiness&&e.currentData.customs_readiness.channel||"Green",depends_on:'eval:doc.action_mode=="C\u1EADp nh\u1EADt tr\u1EA1ng th\xE1i t\u1EDD khai"'},{fieldname:"rejection_reason",fieldtype:"Small Text",label:"L\xFD do t\u1EEB ch\u1ED1i / Ghi ch\xFA (n\u1EBFu Rejected)",depends_on:'eval:doc.action_mode=="C\u1EADp nh\u1EADt tr\u1EA1ng th\xE1i t\u1EDD khai"'},{fieldname:"item_idx",fieldtype:"Int",label:"S\u1ED1 th\u1EE9 t\u1EF1 d\xF2ng h\xE0ng (1-based)",default:1,depends_on:'eval:doc.action_mode!="C\u1EADp nh\u1EADt tr\u1EA1ng th\xE1i t\u1EDD khai"'},{fieldname:"item_description",fieldtype:"Small Text",label:"M\xF4 t\u1EA3 k\u1EF9 thu\u1EADt h\xE0ng h\xF3a (AI/RAG)",depends_on:'eval:doc.action_mode=="G\u1EE3i \xFD m\xE3 HS b\u1EB1ng AI/RAG"'},{fieldname:"use_llm",fieldtype:"Check",label:"K\u1EBFt h\u1EE3p LLM gi\u1EA3i tr\xECnh GIR",default:0,depends_on:'eval:doc.action_mode=="G\u1EE3i \xFD m\xE3 HS b\u1EB1ng AI/RAG"'},{fieldname:"approval_action",fieldtype:"Select",label:"Quy\u1EBFt \u0111\u1ECBnh Chuy\xEAn vi\xEAn",options:`approve
reject`,default:"approve",depends_on:'eval:doc.action_mode=="Ph\xEA duy\u1EC7t / T\u1EEB ch\u1ED1i HS (Chuy\xEAn vi\xEAn)"'},{fieldname:"approved_hs_code",fieldtype:"Data",label:"M\xE3 HS ph\xEA duy\u1EC7t (\u0111\u1EC3 tr\u1ED1ng = x\xE1c nh\u1EADn m\xE3 \u0111\u1EC1 xu\u1EA5t)",depends_on:'eval:doc.action_mode=="Ph\xEA duy\u1EC7t / T\u1EEB ch\u1ED1i HS (Chuy\xEAn vi\xEAn)"'},{fieldname:"approval_notes",fieldtype:"Small Text",label:"Ghi ch\xFA th\u1EA9m \u0111\u1ECBnh chuy\xEAn vi\xEAn",default:"\u0110\xE3 \u0111\u1ED1i chi\u1EBFu bi\u1EC3u thu\u1EBF TT31/2022/TT-BTC.",depends_on:'eval:doc.action_mode=="Ph\xEA duy\u1EC7t / T\u1EEB ch\u1ED1i HS (Chuy\xEAn vi\xEAn)"'}],function(i){if(i.action_mode==="G\u1EE3i \xFD m\xE3 HS b\u1EB1ng AI/RAG"){frappe.call({method:"logistics_wizard.customs_engine.api.suggest_hs_code_with_rag",args:{declaration_name:n,item_idx:i.item_idx||1,item_description:i.item_description||void 0,auto_propose:1,use_llm:i.use_llm?1:0},freeze:!0,freeze_message:__("\u0110ang tra c\u1EE9u AI/RAG & bi\u1EC3u thu\u1EBF HS..."),callback:function(a){let s=a.message||{};if(s.success&&s.primary_recommendation){let l=s.primary_recommendation;frappe.msgprint({title:__(`AI/RAG \u0110\u1EC1 xu\u1EA5t HS: ${l.hs_code} (${l.confidence_score}%)`),indicator:"blue",message:`<p><b>M\xF4 t\u1EA3:</b> ${frappe.utils.escape_html(l.description||"")}</p><p><b>C\u0103n c\u1EE9 ph\xE1p l\xFD:</b> ${frappe.utils.escape_html(l.legal_basis||"")}</p><p style="color:#b45309;"><b>L\u01B0u \xFD ki\u1EC3m so\xE1t:</b> Tr\u1EA1ng th\xE1i \u0111\xE3 l\u01B0u l\xE0 <b>Proposed</b>. Chuy\xEAn vi\xEAn H\u1EA3i quan c\u1EA7n b\u1EA5m <b>Ph\xEA duy\u1EC7t HS</b> tr\u01B0\u1EDBc khi truy\u1EC1n t\u1EDD khai.</p>`}),e.load_case(t)}else frappe.msgprint({title:__("K\u1EBFt qu\u1EA3 AI/RAG"),message:s.error||s.message||"Kh\xF4ng t\xECm th\u1EA5y m\xE3 HS ph\xF9 h\u1EE3p.",indicator:"orange"})}});return}if(i.action_mode==="Ph\xEA duy\u1EC7t / T\u1EEB ch\u1ED1i HS (Chuy\xEAn vi\xEAn)"){frappe.call({method:"logistics_wizard.customs_engine.api.approve_hs_code",args:{declaration_name:n,item_idx:i.item_idx||1,action:i.approval_action||"approve",approved_hs_code:i.approved_hs_code||void 0,notes:i.approval_notes||void 0},callback:function(a){let s=a.message||{};s.success?(frappe.show_alert({message:__(`\u0110\xE3 c\u1EADp nh\u1EADt th\u1EA9m \u0111\u1ECBnh HS d\xF2ng #${s.item_idx}: ${s.hs_approval_status} (${s.approved_hs_code||"N/A"})`),indicator:"green"}),e.load_case(t)):frappe.msgprint({title:__("L\u1ED7i ph\xEA duy\u1EC7t HS"),message:s.error||"Kh\xF4ng th\u1EC3 ph\xEA duy\u1EC7t HS.",indicator:"red"})}});return}frappe.call({method:"logistics_wizard.customs_engine.api.advance_customs_workflow",args:{declaration_name:n,target_status:i.target_status,declaration_no:i.declaration_no||void 0,customs_lane:i.customs_lane,rejection_reason:i.rejection_reason||void 0},callback:function(a){let s=a.message||{};s.success?(frappe.show_alert({message:__(`\u0110\xE3 c\u1EADp nh\u1EADt ${n} \u2192 ${s.workflow_status} (${s.customs_lane})`),indicator:"green"}),e.load_case(t)):frappe.msgprint({title:__("Ch\u1EB7n c\u1EADp nh\u1EADt H\u1EA3i quan"),message:s.error||"Kh\xF4ng th\u1EC3 chuy\u1EC3n tr\u1EA1ng th\xE1i t\u1EDD khai.",indicator:"red"})}})},__(`Thao t\xE1c H\u1EA3i quan & AI/RAG \u2014 ${n}`),__("Th\u1EF1c hi\u1EC7n"))}),$(document).on("click","#btn-add-cost",function(){let t=e.currentData&&e.currentData.case_id||e.currentCaseId;frappe.prompt([{fieldname:"cost_type",fieldtype:"Select",label:"Lo\u1EA1i chi ph\xED (Cost Type)",options:`Freight
Insurance
Duty
Tax
Port
Handling
Storage
Demurrage/Detention
Trucking
Broker Fee
Other`,default:"Freight",reqd:1},{fieldname:"cost_description",fieldtype:"Data",label:"Di\u1EC5n gi\u1EA3i chi ph\xED",reqd:1},{fieldname:"invoice_number",fieldtype:"Data",label:"S\u1ED1 h\xF3a \u0111\u01A1n"},{fieldname:"estimated_cost",fieldtype:"Currency",label:"Chi ph\xED d\u1EF1 to\xE1n (Estimated)",default:0},{fieldname:"actual_cost",fieldtype:"Currency",label:"Chi ph\xED th\u1EF1c t\u1EBF (Actual)",default:0,reqd:1},{fieldname:"status",fieldtype:"Select",label:"Tr\u1EA1ng th\xE1i \u0111\u1ED1i so\xE1t",options:`Draft
Verified`,default:"Verified"}],function(n){frappe.call({method:"logistics_wizard.costing_engine.api.add_cost_item_to_case",args:{case_id:t,cost_type:n.cost_type,cost_description:n.cost_description,invoice_number:n.invoice_number,estimated_cost:n.estimated_cost,actual_cost:n.actual_cost,status:n.status},callback:function(i){let a=i.message||{};a.success?(frappe.show_alert({message:__(`\u0110\xE3 ghi nh\u1EADn chi ph\xED v\xE0o ${a.cost_sheet_name}`),indicator:"green"}),e.load_case(t)):frappe.msgprint({title:__("L\u1ED7i ghi nh\u1EADn chi ph\xED"),message:a.error||"Kh\xF4ng th\u1EC3 l\u01B0u d\xF2ng chi ph\xED.",indicator:"red"})}})},__("Ghi nh\u1EADn H\xF3a \u0111\u01A1n Chi ph\xED (Trade Cost)"),__("L\u01B0u chi ph\xED"))}),$(document).on("click","#btn-create-exception",function(){let t=e.currentData&&e.currentData.case_id||e.currentCaseId;frappe.prompt([{fieldname:"exception_type",fieldtype:"Select",label:"Lo\u1EA1i s\u1EF1 c\u1ED1",options:`ETA Delay
Missing Document
Customs Hold
Customs Overdue
Cost Variance
Demurrage/Detention Risk
Warehouse Discrepancy
Warehouse Not Ready
Stale Tracking`,default:"ETA Delay",reqd:1},{fieldname:"severity",fieldtype:"Select",label:"M\u1EE9c \u0111\u1ED9 nghi\xEAm tr\u1ECDng",options:`Info
Warning
High
Critical`,default:"High",reqd:1},{fieldname:"department",fieldtype:"Select",label:"Ph\xF2ng ban ph\u1EE5 tr\xE1ch",options:`Logistics
Purchasing
Customs
Accounting
Warehouse
Sales`,default:"Logistics"},{fieldname:"title",fieldtype:"Data",label:"Ti\xEAu \u0111\u1EC1 s\u1EF1 c\u1ED1",reqd:1},{fieldname:"description",fieldtype:"Small Text",label:"M\xF4 t\u1EA3 chi ti\u1EBFt",reqd:1},{fieldname:"due_date",fieldtype:"Date",label:"H\u1EA1n x\u1EED l\xFD",default:frappe.datetime.nowdate()}],function(n){frappe.call({method:"logistics_wizard.exception_engine.api.raise_exception_from_rule",args:{case_id:t,rule_code:"",exception_type:n.exception_type,severity:n.severity,title:n.title,description:n.description,department:n.department,source_module:"Manual",due_date:n.due_date},callback:function(i){let a=i.message||{};a.success?(frappe.show_alert({message:__(`\u0110\xE3 khai b\xE1o s\u1EF1 c\u1ED1 ${a.name}`),indicator:"orange"}),e.load_case(t)):frappe.msgprint({title:__("L\u1ED7i t\u1EA1o s\u1EF1 c\u1ED1"),message:a.error||"Kh\xF4ng th\u1EC3 l\u01B0u s\u1EF1 c\u1ED1.",indicator:"red"})}})},__("Khai b\xE1o S\u1EF1 c\u1ED1 V\u1EADn h\xE0nh M\u1EDBi"),__("T\u1EA1o s\u1EF1 c\u1ED1"))}),$(document).on("click","#btn-add-action",function(){let t=e.currentData&&e.currentData.case_id||e.currentCaseId;frappe.prompt([{fieldname:"action",fieldtype:"Data",label:"N\u1ED9i dung h\xE0nh \u0111\u1ED9ng",reqd:1},{fieldname:"department",fieldtype:"Select",label:"Ph\xF2ng ban",options:`Logistics
Customs
Purchasing
Accounting
Warehouse
Sales`,default:"Logistics"},{fieldname:"owner_name",fieldtype:"Data",label:"Ng\u01B0\u1EDDi ph\u1EE5 tr\xE1ch",default:frappe.session&&frappe.session.user||"Administrator"},{fieldname:"priority",fieldtype:"Select",label:"\u01AFu ti\xEAn",options:`Low
Medium
High
Urgent`,default:"Medium"},{fieldname:"due_date",fieldtype:"Date",label:"H\u1EA1n x\u1EED l\xFD",default:frappe.datetime.nowdate()}],function(n){frappe.call({method:"logistics_wizard.exception_engine.api.create_action_item",args:{case_id:t,action_title:n.action,department:n.department,owner_name:n.owner_name,priority:n.priority,due_date:n.due_date},callback:function(i){let a=i.message||{};a.success?(frappe.show_alert({message:__(`\u0110\xE3 th\xEAm \u0111\u1EA7u vi\u1EC7c ${a.name}: ${n.action}`),indicator:"green"}),e.load_case(t)):frappe.msgprint({title:__("L\u1ED7i th\xEAm \u0111\u1EA7u vi\u1EC7c"),message:a.error||"Kh\xF4ng th\u1EC3 l\u01B0u h\xE0nh \u0111\u1ED9ng.",indicator:"red"})}})},__("Th\xEAm H\xE0nh \u0110\u1ED9ng Ti\u1EBFp Theo"),__("L\u01B0u \u0111\u1EA7u vi\u1EC7c"))})}attempt_close_case(){let e=this,t=this.currentData&&this.currentData.quick_actions?this.currentData.quick_actions:{};if(t.can_close)frappe.confirm(`B\u1EA1n c\xF3 ch\u1EAFc ch\u1EAFn mu\u1ED1n \u0111\xF3ng ho\xE0n t\u1EA5t h\u1ED3 s\u01A1 Trade Case <strong>${e.currentData.case_id}</strong>?`,function(){frappe.call({method:"logistics_wizard.api.close_trade_case",args:{case_id:e.currentData.case_id},callback:function(n){n&&n.message&&n.message.success?(frappe.show_alert({message:n.message.message,indicator:"green"}),e.load_case(e.currentData.case_id)):frappe.msgprint(n.message.message||"L\u1ED7i khi \u0111\xF3ng case.")}})});else{let n=(t.close_reasons||[]).map(i=>`<li style="margin-bottom: 4px; color: #b91c1c;">${i}</li>`).join("");frappe.msgprint({title:__("\u26D4 KH\xD4NG TH\u1EC2 \u0110\xD3NG H\u1ED2 S\u01A0 (STAGE GATE CH\u1EB6N)"),message:`
                    <div style="font-size: 13px;">
                        <p>H\u1ED3 s\u01A1 <strong>${e.currentData.case_id}</strong> ch\u01B0a th\u1ECFa m\xE3n c\xE1c ti\xEAu ch\xED ch\u1ED1t ch\u1EB7n \u0111\u1EC3 \u0111\xF3ng case:</p>
                        <ul style="padding-left: 18px; margin: 10px 0;">
                            ${n}
                        </ul>
                        <p style="color: #64748b; font-style: italic;">Vui l\xF2ng ho\xE0n t\u1EA5t b\xE0n giao h\xE0ng, th\xF4ng quan, ch\u1ED1t chi ph\xED v\xE0 gi\u1EA3i quy\u1EBFt tri\u1EC7t \u0111\u1EC3 c\xE1c s\u1EF1 c\u1ED1 tr\u01B0\u1EDBc khi \u0111\xF3ng h\u1ED3 s\u01A1!</p>
                    </div>
                `,indicator:"red"})}}load_case(e){let t=this;this.currentCaseId=e||this.currentCaseId||"",$("#tc-current-case-badge").text(this.currentCaseId||"--"),this.currentCaseId&&$("#tc-case-selector").val()!==this.currentCaseId&&$("#tc-case-selector").val(this.currentCaseId),frappe.call({method:"logistics_wizard.api.get_trade_case_overview_data",args:{case_id:this.currentCaseId||void 0},callback:function(n){if(n&&n.message){let i=n.message.header&&n.message.header.case_id||n.message.case_id||t.currentCaseId;i&&(t.currentCaseId=i,$("#tc-current-case-badge").text(i),$("#tc-case-selector").val(i)),t.currentData=n.message,t.render(n.message)}}})}render(e){if(!e)return;this.currentData=e;let t=e.header||{};$("#tc-id-text, #tc-header-id").text(t.case_id||"--"),$("#tc-status-badge, #tc-header-status").text(t.status?t.status.toUpperCase():"ACTIVE");let n=(t.health||"Attention").toLowerCase(),i=n==="healthy"?"badge-success":n==="critical"?"badge-danger":"badge-warning";if($("#tc-health-badge, #tc-header-health").attr("class",`tc-badge-health ${n} ${i}`).text(`Health: ${(t.health||"Attention").toUpperCase()}`),$("#tc-priority-badge, #tc-header-priority").text(`${t.priority||"Normal"} Priority`),$("#tc-party-text, #tc-meta-party").text(`${t.trade_type||"Import"} Case \u2014 ${t.supplier||t.customer||"N/A"}`),$("#tc-docref-text, #tc-meta-po").html(`<a href="${t.purchase_order?"/app/purchase-order/"+t.purchase_order:"#"}" class="tc-link">${t.purchase_order||t.sales_order||"N/A"}</a>`),$("#tc-mode-incoterm, #tc-meta-mode-incoterm").text(`${t.mode||"Ocean"} \u2022 ${t.incoterm||"FOB"}`),$("#tc-route-text, #tc-meta-route").text(`${t.origin||"N/A"} \u2794 ${t.destination||"N/A"}`),$("#tc-owner-text, #tc-meta-owner").text(`${t.owner||"Nguyen Van A"} (${t.department||"Logistics"})`),$("#tc-expected-close, #tc-meta-expected-close").text(t.expected_close||"N/A"),e.lifecycle){let a=e.lifecycle;$("#tc-current-stage-callout, #tc-lifecycle-current-label").html(`Giai \u0111o\u1EA1n hi\u1EC7n t\u1EA1i: <strong>${a.current_stage||"IN TRANSIT"}</strong>`);let s=$("#tc-lifecycle-stepper");s.empty(),(a.stages||[]).forEach((c,d)=>{let o=c.status,h=`
                    <div class="tc-step-item ${o}">
                        <div class="tc-step-circle">${o==="completed"?"\u2713":o==="current"?"\u25CF":"\u25CB"}</div>
                        <div class="tc-step-label">${c.label}</div>
                    </div>
                `;s.append(h)}),a.previous_milestone&&($("#tc-prev-ms-title, #tc-ms-prev-title").text(a.previous_milestone.title),$("#tc-prev-ms-date, #tc-ms-prev-date").text(a.previous_milestone.date)),a.next_milestone&&($("#tc-next-ms-title, #tc-ms-next-title").text(a.next_milestone.title),$("#tc-next-ms-date, #tc-ms-next-date").text(a.next_milestone.eta))}if(e.overall_health&&e.overall_health.cards){let a=$("#tc-health-grid");a.empty(),e.overall_health.cards.forEach(s=>{let l=`
                    <div class="tc-health-card ${s.class||"neutral"}">
                        <div class="tc-hc-label">${s.label}</div>
                        <div class="tc-hc-val">${s.value}</div>
                        <div class="tc-hc-sub">${s.sub}</div>
                    </div>
                `;a.append(l)})}if(e.shipment_summary){let a=e.shipment_summary,s=a.total_shipments>1?`<div style="margin-top: 8px; font-size: 11px; color: #64748b; font-weight: 600;">T\u1ED5ng s\u1ED1: <strong>${a.total_shipments} Shipments</strong> (${a.shipment_counts.in_transit} \u0110ang \u0111i, ${a.shipment_counts.delivered} \u0110\xE3 \u0111\u1EBFn)</div>`:"",l=`
                <table class="tc-kv-table">
                    <tr><td class="tc-kv-key">M\xE3 v\u1EADn \u0111\u01A1n (Shipment ID):</td><td class="tc-kv-val font-weight-bold text-primary">${a.shipment_id||"N/A"}</td></tr>
                    <tr><td class="tc-kv-key">H\xE3ng v\u1EADn t\u1EA3i (Carrier):</td><td class="tc-kv-val">${a.carrier||"N/A"}</td></tr>
                    <tr><td class="tc-kv-key">T\xEAn ph\u01B0\u01A1ng ti\u1EC7n (Vessel/Flight):</td><td class="tc-kv-val">${a.vessel||"N/A"}</td></tr>
                    <tr><td class="tc-kv-key">S\u1ED1 l\u01B0\u1EE3ng Container:</td><td class="tc-kv-val">${a.container_count||1} Containers</td></tr>
                    <tr><td class="tc-kv-key">C\u1EA3ng xu\u1EA5t (POL):</td><td class="tc-kv-val">${a.pol||"N/A"}</td></tr>
                    <tr><td class="tc-kv-key">C\u1EA3ng nh\u1EADp (POD):</td><td class="tc-kv-val">${a.pod||"N/A"}</td></tr>
                    <tr><td class="tc-kv-key">Ng\xE0y kh\u1EDFi h\xE0nh (ATD):</td><td class="tc-kv-val">${a.atd||"N/A"}</td></tr>
                    <tr><td class="tc-kv-key">L\u1ECBch d\u1EF1 ki\u1EBFn ban \u0111\u1EA7u (Original ETA):</td><td class="tc-kv-val">${a.original_eta||"N/A"}</td></tr>
                    <tr><td class="tc-kv-key">ETA hi\u1EC7n t\u1EA1i:</td><td class="tc-kv-val text-primary font-weight-bold">${a.current_eta||"N/A"}</td></tr>
                    <tr><td class="tc-kv-key">\u0110\u1ED9 tr\u1EC5 h\xE0nh tr\xECnh (Delay):</td><td class="tc-kv-val ${a.delay_days>0?"text-danger":"text-success"} font-weight-bold">${a.delay_days>0?"+"+a.delay_days+" ng\xE0y (Delay)":"\u0110\xFAng h\u1EA1n (On-time)"}</td></tr>
                </table>
                ${s}
            `;$("#tc-shipment-summary-body, #tc-shipment-body").html(l)}if(e.document_readiness){let a=e.document_readiness;$("#tc-doc-readiness-badge, #tc-docs-pct-badge").text(`${a.ready_count} / ${a.total_count} S\u1EB5n s\xE0ng (${a.percentage}%)`);let s="";a.missing_urgent&&a.missing_urgent.length>0&&(s=a.missing_urgent.map(c=>`
                    <div class="tc-urgent-doc-alert">
                        <strong>\u26A0 Thi\u1EBFu kh\u1EA9n c\u1EA5p: ${c.name}</strong><br>
                        <span style="font-size: 11px;">H\u1EA1n ch\xF3t: ${c.deadline} \u2022 ${c.note}</span>
                    </div>
                `).join(""));let l=(a.categories||[]).map(c=>`
                <div class="tc-doc-cat-box">
                    <span>${c.name}</span>
                    <span class="${c.status==="completed"?"text-success":"text-warning"} font-weight-bold">
                        ${c.ready}/${c.total} ${c.status==="completed"?"\u2713":"\u26A0"}
                    </span>
                </div>
            `).join("");$("#tc-doc-readiness-body, #tc-docs-body").html(`
                ${s}
                <div class="progress" style="height: 10px; margin-bottom: 12px; border-radius: 5px;">
                    <div class="progress-bar ${a.percentage===100?"bg-success":"bg-warning"}" style="width: ${a.percentage}%;"></div>
                </div>
                <div class="tc-doc-cat-grid">
                    ${l}
                </div>
                <div style="margin-top: 14px; text-align: right;">
                    <button class="btn btn-xs btn-default" id="tc-btn-view-docs"><i class="fa fa-folder-open-o"></i> Qu\u1EA3n l\xFD H\u1ED3 s\u01A1 Chi ti\u1EBFt</button>
                </div>
            `)}if(e.customs_readiness){let a=e.customs_readiness;$("#tc-customs-badge, #tc-customs-status-badge").text(`${a.status} (${a.readiness_pct}%)`),$("#tc-customs-body").html(`
                <table class="tc-kv-table">
                    <tr><td class="tc-kv-key">M\xE3 ph\xE2n lo\u1EA1i HS:</td><td class="tc-kv-val font-weight-bold">${a.hs_classification}</td></tr>
                    <tr><td class="tc-kv-key">Tr\u1EA1ng th\xE1i ph\xEA duy\u1EC7t HS:</td><td class="tc-kv-val text-success">\u2713 ${a.hs_approval_status}</td></tr>
                    <tr><td class="tc-kv-key">X\xE1c th\u1EF1c Xu\u1EA5t x\u1EE9 (Origin):</td><td class="tc-kv-val text-success">${a.origin_verified?"\u2713 \u0110\xE3 x\xE1c th\u1EF1c":"Ch\u01B0a x\xE1c th\u1EF1c"}</td></tr>
                    <tr><td class="tc-kv-key">Tr\u1ECB gi\xE1 H\u1EA3i quan (Value):</td><td class="tc-kv-val text-success">${a.customs_value_verified?"\u2713 \u0110\xE3 x\xE1c th\u1EF1c":"Ch\u01B0a x\xE1c th\u1EF1c"}</td></tr>
                    <tr><td class="tc-kv-key">T\u1EDD khai H\u1EA3i quan (Declaration):</td><td class="tc-kv-val text-warning font-weight-bold">${a.declaration_status}</td></tr>
                    <tr><td class="tc-kv-key">Gi\u1EA5y ph\xE9p chuy\xEAn ng\xE0nh:</td><td class="tc-kv-val">${a.license}</td></tr>
                    <tr><td class="tc-kv-key">Ki\u1EC3m tra chuy\xEAn ng\xE0nh:</td><td class="tc-kv-val">${a.inspection}</td></tr>
                    <tr><td class="tc-kv-key">T\xECnh tr\u1EA1ng Th\xF4ng quan:</td><td class="tc-kv-val ${a.clearance_status==="CLEARED"?"text-success font-weight-bold":"text-danger font-weight-bold"}">${a.clearance_status}</td></tr>
                </table>
            `)}if(e.cost_summary){let a=e.cost_summary,s=e.header&&String(e.header.trade_type||"").toLowerCase()==="export",l=s?"Tr\u1ECB gi\xE1 L\xF4 xu\u1EA5t (SO/SI)":"Tr\u1ECB gi\xE1 H\xE0ng mua (PO)",c=s?"Chi ph\xED Xu\u1EA5t kh\u1EA9u Th\u1EF1c t\u1EBF":"T\u1ED5ng Chi ph\xED Logistics Th\u1EF1c t\u1EBF",d=a.variance_amount>=0?"+":"",o=a.variance_amount>0?"text-danger":"text-success";$("#tc-cost-status-badge").text(`${a.cost_finalization_status} (${d}${a.variance_pct}%)`);let r=(a.breakdown||[]).map(h=>`
                <tr>
                    <td style="padding: 4px 0; color: #64748b;">${h.label}</td>
                    <td style="padding: 4px 0; text-align: right; font-weight: 600;">$${Number(h.amount||0).toLocaleString()}</td>
                </tr>
            `).join("");$("#tc-cost-body").html(`
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 12px; background: #f8fafc; padding: 10px; border-radius: 6px; border: 1px solid #e2e8f0;">
                    <div>
                        <div style="font-size: 11px; color: #64748b;">${l}</div>
                        <div style="font-size: 14px; font-weight: 800; color: #0f172a;">$${Number(a.purchase_value||0).toLocaleString()}</div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #64748b;">D\u1EF1 to\xE1n: $${Number(a.estimated_cost||0).toLocaleString()}</div>
                        <div style="font-size: 14px; font-weight: 800;" class="${o}">
                            $${Number(a.actual_cost||0).toLocaleString()} <span style="font-size: 11px;">(${d}${a.variance_pct}%)</span>
                        </div>
                    </div>
                    <div>
                        <div style="font-size: 11px; color: #64748b;">${s?"Ch\xEAnh l\u1EC7ch D\u1EF1 to\xE1n":"T\u1ED5ng Landed Cost"}</div>
                        <div style="font-size: 14px; font-weight: 800; color: #0f766e;">
                            ${s?d+"$"+Number(a.variance_amount||0).toLocaleString():"$"+Number(a.actual_landed_cost||0).toLocaleString()}
                        </div>
                    </div>
                </div>
                <div style="font-size: 12px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">${c} Theo Nh\xF3m:</div>
                <table style="width: 100%; font-size: 12px; margin-bottom: 12px;">
                    ${r}
                </table>
                <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748b; border-top: 1px dashed #e2e8f0; padding-top: 8px;">
                    <span>H\xF3a \u0111\u01A1n nh\u1EADn: <strong>${a.invoices_received}/${a.invoices_total}</strong></span>
                    <span>\u0110\xE3 th\u1EA9m \u0111\u1ECBnh: <strong>${a.costs_verified}/${a.invoices_total}</strong></span>
                    <span>\u0110\xE3 ph\xE2n b\u1ED5 LCV: <strong>${a.costs_allocated}/${a.invoices_total}</strong></span>
                </div>
            `)}if(e.warehouse_readiness){let a=e.warehouse_readiness;$("#tc-wh-badge, #tc-warehouse-status-badge").text(a.receiving_status);let s=a.discrepancy_alert?'<div class="tc-urgent-doc-alert">\u26A0 PH\xC1T HI\u1EC6N L\u1EC6CH S\u1ED0 L\u01AF\u1EE2NG / H\u01AF H\u1ECENG H\xC0NG H\xD3A!</div>':"";$("#tc-wh-body, #tc-warehouse-body").html(`
                ${s}
                <table class="tc-kv-table">
                    <tr><td class="tc-kv-key">L\u1ECBch d\u1EF1 ki\u1EBFn nh\u1EADp kho:</td><td class="tc-kv-val font-weight-bold">${a.expected_arrival}</td></tr>
                    <tr><td class="tc-kv-key">\u0110\u1ECBa \u0111i\u1EC3m Kho nh\u1EADn:</td><td class="tc-kv-val">${a.warehouse}</td></tr>
                    <tr><td class="tc-kv-key">Tr\u1EA1ng th\xE1i Ti\u1EBFp nh\u1EADn:</td><td class="tc-kv-val text-warning font-weight-bold">${a.receiving_status}</td></tr>
                    <tr><td class="tc-kv-key">S\u1ED1 l\u01B0\u1EE3ng d\u1EF1 ki\u1EBFn (Expected):</td><td class="tc-kv-val">${a.expected_qty?a.expected_qty.toLocaleString():"N/A"} ki\u1EC7n</td></tr>
                    <tr><td class="tc-kv-key">M\u1EB7t b\u1EB1ng kho d\u1EF1 tr\u1EEF:</td><td class="tc-kv-val text-success">${a.space_reserved?"\u2713 \u0110\xE3 gi\u1EEF ch\u1ED7 s\u1EB5n s\xE0ng":"Ch\u01B0a b\u1ED1 tr\xED"}</td></tr>
                    <tr><td class="tc-kv-key">\u0110\u1ED9i ng\u0169 ti\u1EBFp nh\u1EADn:</td><td class="tc-kv-val">${a.receiving_team}</td></tr>
                </table>
            `)}if(e.open_exceptions){let a=e.open_exceptions;$("#tc-exceptions-badge, #tc-open-exceptions-badge").text(`${a.total_open} Open (${a.overdue} Qu\xE1 h\u1EA1n)`);let s=(a.items||[]).map(l=>{let c=(l.severity||"medium").toLowerCase();return`
                    <div class="tc-exception-item ${c}">
                        <div class="tc-exc-header">
                            <span class="badge ${c==="high"||c==="critical"?"badge-danger":"badge-warning"}">${l.severity}</span>
                            <span style="color: #64748b;">${l.id}</span>
                        </div>
                        <div class="tc-exc-title">${l.title}</div>
                        <div class="tc-exc-meta">
                            <span><i class="fa fa-user"></i> ${l.owner} (${l.department})</span>
                            <span><i class="fa fa-clock-o"></i> H\u1EA1n: ${l.due_date}</span>
                            <span class="font-weight-bold text-primary">${l.status}</span>
                        </div>
                    </div>
                `}).join("");s||(s='<div class="text-center text-success" style="padding: 20px;"><i class="fa fa-check-circle" style="font-size: 24px;"></i><p style="margin-top: 6px; font-weight: 600;">Kh\xF4ng c\xF3 s\u1EF1 c\u1ED1 n\xE0o \u0111ang m\u1EDF.</p></div>'),$("#tc-exceptions-body").html(s)}if(e.upcoming_actions){let a=e.upcoming_actions.map(s=>`
                <div class="tc-action-item">
                    <div class="tc-action-date">${s.date}</div>
                    <div class="tc-action-desc">${s.action}</div>
                    <div class="tc-action-dept"><span class="badge badge-default">${s.department}</span> (${s.owner})</div>
                </div>
            `).join("");$("#tc-actions-body").html(a||'<div class="text-muted">Kh\xF4ng c\xF3 l\u1ECBch h\xE0nh \u0111\u1ED9ng ti\u1EBFp theo.</div>')}if(e.related_erp_documents){let a=e.related_erp_documents.map(s=>`
                <tr>
                    <td style="padding: 6px 0; font-weight: 600; color: #64748b;">${s.doctype}</td>
                    <td style="padding: 6px 0;"><a href="${s.link}" class="tc-link font-weight-bold">${s.name}</a></td>
                    <td style="padding: 6px 0; text-align: right;">
                        <span class="tc-badge-erp ${s.status==="Submitted"||s.status==="Completed"?"submitted":"pending"}">${s.status}</span>
                    </td>
                </tr>
            `).join("");$("#tc-related-erp-body").html(`<table style="width: 100%; font-size: 12px;">${a}</table>`)}if(e.responsibility_matrix){let a=e.responsibility_matrix.map(s=>`
                <tr>
                    <td style="padding: 6px 0; font-weight: 700; color: #0284c7;">${s.role}</td>
                    <td style="padding: 6px 0; font-weight: 600; color: #0f172a;">${s.name}</td>
                    <td style="padding: 6px 0; color: #64748b; font-size: 11px;">${s.department}</td>
                </tr>
            `).join("");$("#tc-responsibility-body").html(`<table style="width: 100%; font-size: 12px;">${a}</table>`)}if(e.activity_timeline){let a=e.activity_timeline.map(s=>`
                <div class="tc-timeline-event">
                    <div class="tc-event-time">${s.time}</div>
                    <div class="tc-event-desc">
                        <strong style="color: #0284c7;">${s.actor}:</strong> ${s.event}
                    </div>
                </div>
            `).join("");$("#tc-activity-body").html(a||'<div class="text-muted">Ch\u01B0a c\xF3 nh\u1EADt k\xFD ho\u1EA1t \u0111\u1ED9ng.</div>')}if(e.quick_actions){let s=(e.quick_actions.close_reasons||[]).map(l=>`<div class="tc-sg-rule">${l}</div>`).join("");$("#tc-stage-gate-body").html(`
                <div class="tc-action-btn-group">
                    <button class="btn btn-default" id="btn-upload-doc"><i class="fa fa-upload"></i> Upload Document</button>
                    <button class="btn btn-default" id="btn-update-customs"><i class="fa fa-check-circle"></i> Update Customs</button>
                    <button class="btn btn-default" id="btn-add-cost"><i class="fa fa-dollar-sign"></i> Add Cost</button>
                    <button class="btn btn-default" id="btn-create-exception"><i class="fa fa-exclamation-triangle"></i> Create Exception</button>
                    <button class="btn btn-default" id="btn-add-action"><i class="fa fa-plus"></i> Add Action</button>
                </div>
                <div class="tc-stage-gate-box">
                    <div class="tc-sg-title">
                        <i class="fa fa-lock"></i> \u0110I\u1EC0U KI\u1EC6N CH\u1ED0T CH\u1EB6N \u0110\xD3NG CASE (STAGE GATE)
                    </div>
                    ${s}
                    <div style="margin-top: 10px; display: flex; justify-content: flex-end;">
                        <button class="btn btn-sm btn-danger font-weight-bold" id="tc-btn-close-case">
                            <i class="fa fa-check-square-o"></i> \u0110\xF3ng Trade Case (Close Case)
                        </button>
                    </div>
                </div>
            `)}}},F=class{constructor(e,t){this.wrapper=e,this.pageName=t||"trade-case-overview",e&&typeof frappe!="undefined"&&frappe.ui&&frappe.ui.make_app_page&&(this.page=frappe.ui.make_app_page({parent:e,title:__("Trade Case Dossier"),single_column:!0}),this.page&&this.page.container&&(this.page.container.removeClass("container").addClass("container-fluid"),this.page.container.css({"max-width":"100%",padding:"0",margin:"0"})),q(e)),this.data=null,this.selectedShipment=null,this.pendingFocusShipment=null,this.currentFilter="all",this.searchTerm="",this.map=null,this.mapLayers={baseLand:null,seaOverlay:null,routePolylines:[],markers:[],vehicleMarker:null,fleetVehicleMarkers:[]},this.debounceTimer=null,e&&this.init()}init(){this.render_skeleton(this.pageName),this.bind_events(),this.init_map(),this.refresh()}render_skeleton(e){let t=window.UNIFIED_LOGISTICS_HUB_HTML||"";if(!t&&frappe.templates){let n=[e,e?e.replace(/-/g,"_"):null,"trade_case_overview","managementlogistic","managementLogistic","shipment_tracking_hub"];for(let i of n)if(i&&frappe.templates[i]){t=frappe.render_template(i,{});break}}this.page&&this.page.body?$(this.page.body).html(t):this.wrapper&&$(this.wrapper).html(t)}bind_events(){let e=this;$("#hub-btn-refresh").on("click",function(){$(this).find("i").addClass("fa-spin"),e.refresh(e.selectedShipment?e.selectedShipment.name:null,()=>{$("#hub-btn-refresh").find("i").removeClass("fa-spin")})}),$("#hub-btn-sync-now").on("click",function(){let t=e.selectedShipment?e.selectedShipment.name:null;e.sync_now(t)}),$(".hub-kpi-card").on("click",function(){let t=$(this).data("filter");$(".hub-kpi-card").removeClass("active"),$(this).addClass("active"),$(".hub-tab-btn").removeClass("active"),$(`.hub-tab-btn[data-tab="${t}"]`).addClass("active"),e.currentFilter=t,e.filter_and_render_table()}),$(".hub-tab-btn").on("click",function(){let t=$(this).data("tab");$(".hub-tab-btn").removeClass("active"),$(this).addClass("active"),$(".hub-kpi-card").removeClass("active"),$(`.hub-kpi-card[data-filter="${t}"]`).addClass("active"),e.currentFilter=t,e.filter_and_render_table()}),$("#hub-search-input").on("input",function(){clearTimeout(e.debounceTimer),e.debounceTimer=setTimeout(()=>{e.searchTerm=($(this).val()||"").trim().toLowerCase(),e.filter_and_render_table()},250)}),$("#hub-map-reset-btn").on("click",function(){e.reset_map_view()})}init_map(){let e=this,t=window.L||window.leaflet;if(!t){console.warn("[TrackingHub] Leaflet is not loaded yet");return}let n=this.wrapper?$(this.wrapper).find("#lw-hub-map"):$("#lw-hub-map");if(!n.length)return;let i=n[0];if(i._leaflet_id){try{if(this.map){this.map.invalidateSize();return}}catch(a){}try{i._leaflet_id=null}catch(a){}}try{this.map=t.map(i,{center:[22,150],zoom:3,minZoom:2,maxZoom:18,zoomControl:!0,attributionControl:!0}),t.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{attribution:"&copy; OpenStreetMap contributors",maxZoom:18,subdomains:["a","b","c"]}).addTo(this.map),setTimeout(()=>{e.map&&e.map.invalidateSize()},300)}catch(a){console.error("[TrackingHub] Error initializing map:",a)}}refresh(e=null,t=null){let n=this,i=e||this.pendingFocusShipment;frappe.call({method:"logistics_wizard.api.get_shipment_tracking_hub_data",args:i?{shipment:i}:{},callback:a=>{if(a&&a.message){this.data=a.message,this.render_all(i);let s=this.pendingFocusShipment||i;this.pendingFocusShipment=null,s&&this.select_shipment(s)}t&&t()},error:function(){t&&t()}})}render_all(e=null){if(!this.data)return;this.render_kpis(this.data.kpis||{});let t=this.data.shipments||[];e?this.selectedShipment=t.find(n=>n.name===e||n.purchase_order===e||n.tracking_number===e||n.container_id===e)||this.data.selected_shipment||null:this.selectedShipment=null,this.filter_and_render_table(),this.render_stepper(this.selectedShipment),this.render_exceptions(this.data.active_exceptions||[]),this.update_map_view(this.selectedShipment)}render_kpis(e){$("#kpi-val-total").text(e.total_shipments||0),$("#kpi-val-transit").text(e.in_transit||0),$("#kpi-val-delayed").text(e.delayed_exceptions||0),$("#kpi-val-stale").text(e.stale_tracking||0),$("#tab-cnt-all").text(e.total_shipments||0),$("#tab-cnt-transit").text(e.in_transit||0),$("#tab-cnt-delayed").text(e.delayed_exceptions||0),$("#tab-cnt-stale").text(e.stale_tracking||0);let t=(this.data.shipments||[]).filter(n=>n.status==="Delivered"||n.status==="Completed").length;$("#tab-cnt-delivered").text(t)}filter_and_render_table(){let e=this,t=this.data?this.data.shipments||[]:[];if(this.currentFilter==="In Transit"?t=t.filter(i=>i.status==="In Transit"):this.currentFilter==="Delayed"?t=t.filter(i=>i.is_delayed==1||i.status==="Delayed"):this.currentFilter==="Stale"?t=t.filter(i=>i.is_stale==1):this.currentFilter==="Delivered"&&(t=t.filter(i=>i.status==="Delivered"||i.status==="Completed")),this.searchTerm){let i=this.searchTerm;t=t.filter(a=>a.name&&a.name.toLowerCase().includes(i)||a.tracking_number&&a.tracking_number.toLowerCase().includes(i)||a.container_id&&a.container_id.toLowerCase().includes(i)||a.carrier&&a.carrier.toLowerCase().includes(i)||a.purchase_order&&a.purchase_order.toLowerCase().includes(i)||a.origin_port&&a.origin_port.toLowerCase().includes(i)||a.destination_port&&a.destination_port.toLowerCase().includes(i))}let n=$("#hub-shipments-tbody");if(n.empty(),t.length===0){n.html(`
                <tr>
                    <td colspan="6" class="text-center text-muted" style="padding: 30px;">
                        Kh\xF4ng t\xECm th\u1EA5y l\xF4 h\xE0ng n\xE0o ph\xF9 h\u1EE3p v\u1EDBi b\u1ED9 l\u1ECDc.
                    </td>
                </tr>
            `);return}t.forEach(i=>{let a=e.selectedShipment&&e.selectedShipment.name===i.name,s=i.current_vehicle||e.get_active_vehicle_mode(i,i.progress),l=s==="Air"||s==="Plane"?"\u2708\uFE0F":s==="Ocean"||s==="Ship"?"\u{1F6A2}":"\u{1F69A}",c="badge-in-transit";i.status==="Delayed"||i.is_delayed==1?c="badge-delayed":i.status==="Delivered"||i.status==="Completed"?c="badge-delivered":i.is_stale==1?c="badge-stale":i.status==="Draft"&&(c="badge-draft");let d='<span class="delay-tag-ontime">\u0110\xFAng h\u1EA1n</span>';i.delay_days&&i.delay_days>0&&(d=`<span class="delay-tag-positive">+${i.delay_days} ng\xE0y</span>`);let o=$(`
                <tr class="hub-row-clickable ${a?"selected":""}" data-name="${i.name}">
                    <td>
                        <div style="font-weight: 700; color: #0284c7;">
                            ${l} ${i.name}
                        </div>
                        <div style="font-size: 11px; color: #64748b; font-family: monospace;">
                            ${i.container_id?"Cont: "+i.container_id:i.tracking_number?"Track: "+i.tracking_number:""}
                        </div>
                    </td>
                    <td>
                        <div style="font-weight: 600;">${i.carrier||"Ch\u01B0a ch\u1EC9 \u0111\u1ECBnh"}</div>
                        <div style="font-size: 11px; color: #64748b;">${i.vessel_name||i.flight_number||""}</div>
                    </td>
                    <td>
                        <div style="font-weight: 500;">${i.origin_port||"N/A"} \u2794 ${i.destination_port||"N/A"}</div>
                        <div style="margin-top: 2px;"><span class="badge-status ${c}">${i.status}</span></div>
                    </td>
                    <td>
                        <div style="font-size: 11px;">ETD: ${i.atd||i.etd||"\u2014"}</div>
                        <div style="font-size: 11px; font-weight: 600; color: ${i.is_delayed?"#dc2626":"#1e293b"};">
                            ETA: ${i.eta||"\u2014"}
                        </div>
                    </td>
                    <td>${d}</td>
                    <td style="text-align: center;">
                        <button class="btn btn-xs btn-default hub-btn-select-shipment" data-name="${i.name}" title="Xem l\u1ED9 tr\xECnh tr\xEAn b\u1EA3n \u0111\u1ED3">
                            <i class="fa fa-crosshairs"></i>
                        </button>
                        ${i.purchase_order?`
                            <a href="/app/purchase-order/${i.purchase_order}" class="btn btn-xs btn-default" title="Xem PO ${i.purchase_order}">
                                <i class="fa fa-file-text-o"></i>
                            </a>
                        `:""}
                    </td>
                </tr>
            `);o.on("click",function(r){if($(r.target).closest("a").length)return;e.selectedShipment&&e.selectedShipment.name===i.name?e.reset_map_view():e.select_shipment(i.name)}),o.find(".hub-btn-select-shipment").on("click",function(r){r.stopPropagation(),e.selectedShipment&&e.selectedShipment.name===i.name?e.reset_map_view():e.select_shipment(i.name)}),n.append(o)})}select_shipment(e){let t=this,n=(this.data&&this.data.shipments?this.data.shipments:[]).find(i=>i.name===e);n?this.selectedShipment=n:this.pendingFocusShipment=e,frappe.call({method:"logistics_wizard.api.get_shipment_tracking_hub_data",args:{shipment:e},callback:function(i){i&&i.message&&i.message.selected_shipment&&(t.selectedShipment=i.message.selected_shipment),$("#hub-shipments-tbody tr").removeClass("selected"),$(`#hub-shipments-tbody tr[data-name="${e}"]`).addClass("selected"),t.render_stepper(t.selectedShipment),t.update_map_view(t.selectedShipment)}})}render_stepper(e){let t=$("#hub-stepper-track");if(t.empty(),!e){$("#stepper-shipment-name").text("Ch\u01B0a ch\u1ECDn l\xF4 h\xE0ng"),t.html(`
                <div class="hub-stepper-empty-hint">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#0071E3" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="16" x2="12" y2="12"/>
                        <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                    \u0110ang \u1EDF ch\u1EBF \u0111\u1ED9 <b>To\xE0n c\u1EA3nh</b>. Ch\u1ECDn m\u1ED9t l\xF4 h\xE0ng t\u1EEB danh s\xE1ch b\xEAn d\u01B0\u1EDBi ho\u1EB7c nh\u1EA5p v\xE0o ph\u01B0\u01A1ng ti\u1EC7n tr\xEAn b\u1EA3n \u0111\u1ED3 \u0111\u1EC3 theo d\xF5i chi ti\u1EBFt 9 m\u1ED1c DCSA.
                </div>
            `);return}$("#stepper-shipment-name").text(`${e.name} (${e.carrier||""})`);let n=[{key:"BOOKED",label:"1. \u0110\u1EB7t ch\u1ED7"},{key:"GATE_IN",label:"2. V\xE0o b\xE3i"},{key:"LOADED",label:"3. X\u1EBFp h\xE0ng"},{key:"DEPARTED",label:"4. Kh\u1EDFi h\xE0nh"},{key:"TRANSSHIPMENT",label:"5. Trung chuy\u1EC3n"},{key:"ARRIVED",label:"6. C\u1EADp c\u1EA3ng"},{key:"DISCHARGED",label:"7. D\u1EE1 h\xE0ng"},{key:"GATE_OUT",label:"8. Ra c\u1ED5ng"},{key:"DELIVERED",label:"9. Giao kho"}],i=e.transit_route||[],a=new Set,s={};i.forEach(c=>{c.milestone&&(a.add(c.milestone.toUpperCase()),s[c.milestone.toUpperCase()]=c.date||c.timestamp||"")});let l=-1;for(let c=n.length-1;c>=0;c--)if(a.has(n[c].key)){l=c;break}l===-1&&(l=0),n.forEach((c,d)=>{let o=a.has(c.key),r=d===l,h=e.is_delayed==1,v="";o&&(v+=" completed"),r&&(v+=" current"),h&&(v+=" delayed");let f=s[c.key]?s[c.key].split("T")[0]:"";t.append(`
                <div class="hub-step-item ${v}">
                    <div class="hub-step-badge">
                        ${o?"\u2714":d+1}
                    </div>
                    <div class="hub-step-title">${c.label}</div>
                    <div class="hub-step-date">${f||(r?"\u0110ang th\u1EF1c hi\u1EC7n":"\u2014")}</div>
                </div>
            `)})}render_exceptions(e){let t=$("#hub-exceptions-list");t.empty();let n=e?e.length:0;if($("#hub-exception-count-badge").text(`${n} s\u1EF1 c\u1ED1`),!e||e.length===0){t.html(`
                <div class="text-center text-muted" style="padding: 35px 15px;">
                    <i class="fa fa-check-circle text-success" style="font-size: 28px; margin-bottom: 8px;"></i>
                    <p style="margin: 0; font-size: 13px;">Kh\xF4ng c\xF3 s\u1EF1 c\u1ED1 ho\u1EB7c c\u1EA3nh b\xE1o ngo\u1EA1i l\u1EC7 \u0111ang m\u1EDF.</p>
                </div>
            `);return}e.forEach(i=>{let a=i.severity==="Critical",s=a?"badge-danger":"badge-warning",l=a?"\u{1F534}":"\u{1F7E1}";t.append(`
                <div class="hub-exception-card ${a?"critical":"warning"}">
                    <div class="exception-card-header">
                        <span class="exception-title">${l} ${i.exception_type||"Ngo\u1EA1i l\u1EC7 V\u1EADn chuy\u1EC3n"}</span>
                        <span class="badge ${s}">${i.severity}</span>
                    </div>
                    <div class="exception-card-body">
                        <div><strong>L\xF4 h\xE0ng:</strong> ${i.shipment_tracking}</div>
                        ${i.purchase_order?`<div><strong>\u0110\u01A1n h\xE0ng:</strong> ${i.purchase_order}</div>`:""}
                        ${i.old_eta&&i.new_eta?`
                            <div class="exception-timeline-shift">
                                <span>ETA: ${i.old_eta} \u2794 <strong>${i.new_eta}</strong></span>
                                <span class="badge-status badge-delayed">+${i.delay_days||0} ng\xE0y</span>
                            </div>
                        `:""}
                        <div style="margin-top: 6px; color: #475569;">${i.description||""}</div>
                    </div>
                    <div class="exception-card-footer">
                        ${i.purchase_order?`
                            <a href="/app/purchase-order/${i.purchase_order}" class="btn btn-xs btn-default">
                                <i class="fa fa-external-link"></i> M\u1EDF PO
                            </a>
                        `:""}
                        <button class="btn btn-xs btn-primary hub-btn-resolve-exc" data-name="${i.name}">
                            \u0110\xE1nh d\u1EA5u \u0111\xE3 x\u1EED l\xFD
                        </button>
                    </div>
                </div>
            `)}),$(".hub-btn-resolve-exc").on("click",function(){let i=$(this).data("name");frappe.db.set_value("Shipment Exception",i,"status","Resolved").then(()=>{frappe.show_alert({message:__("\u0110\xE3 gi\u1EA3i quy\u1EBFt ngo\u1EA1i l\u1EC7!"),indicator:"green"}),$(this).closest(".hub-exception-card").fadeOut(300,function(){$(this).remove()})})})}update_marine_overlay(e){if(!this.map)return;let t=window.L||window.leaflet;!t||(e==="Ocean"?(this.mapLayers.seaOverlay||(this.mapLayers.seaOverlay=t.tileLayer("https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png",{attribution:'H\u1EA3i \u0111\u1ED3 &copy; <a href="http://www.openseamap.org">OpenSeaMap</a>',maxZoom:18,opacity:.95})),this.map.hasLayer(this.mapLayers.seaOverlay)||this.mapLayers.seaOverlay.addTo(this.map)):this.mapLayers.seaOverlay&&this.map.hasLayer(this.mapLayers.seaOverlay)&&this.map.removeLayer(this.mapLayers.seaOverlay))}get_vehicle_svg(e){return e==="Air"?`
                <svg width="24" height="24" viewBox="0 0 24 24" fill="#007AFF" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 1.5C11.2 1.5 10.6 2.3 10.6 3.2V8.8L2.4 13.5C1.8 13.8 1.5 14.5 1.5 15.1C1.5 15.9 2.2 16.5 3 16.5H10.6V20.2L8.2 21.8C7.9 22 7.7 22.3 7.7 22.7C7.7 23.4 8.3 24 9 24H15C15.7 24 16.3 23.4 16.3 22.7C16.3 22.3 16.1 22 15.8 21.8L13.4 20.2V16.5H21C21.8 16.5 22.5 15.9 22.5 15.1C22.5 14.5 22.2 13.8 21.6 13.5L13.4 8.8V3.2C13.4 2.3 12.8 1.5 12 1.5Z" stroke="#0047AB" stroke-width="0.5"/>
                </svg>
            `:e==="Ocean"?`
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 1 C14.8 3.5 18 8 18 14 V20 C18 21.7 16.7 23 15 23 H9 C7.3 23 6 21.7 6 20 V14 C6 8 9.2 3.5 12 1 Z" fill="#0055B3" stroke="#003380" stroke-width="0.8"/>
                    <rect x="8" y="6.5" width="8" height="2.2" rx="0.4" fill="#38BDF8"/>
                    <rect x="8" y="9.7" width="8" height="2.2" rx="0.4" fill="#BAE6FD"/>
                    <rect x="8" y="12.9" width="8" height="2.2" rx="0.4" fill="#38BDF8"/>
                    <rect x="8" y="16.1" width="8" height="2.2" rx="0.4" fill="#BAE6FD"/>
                    <rect x="8.5" y="19.2" width="7" height="2.6" rx="0.5" fill="#FFFFFF"/>
                    <rect x="10.5" y="20" width="3" height="1" fill="#0055B3"/>
                </svg>
            `:`
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="6" y="8.5" width="12" height="14" rx="1.2" fill="#EA580C" stroke="#C2410C" stroke-width="0.6"/>
                    <line x1="7.5" y1="11.5" x2="16.5" y2="11.5" stroke="#FFEDD5" stroke-width="0.8"/>
                    <line x1="7.5" y1="14.5" x2="16.5" y2="14.5" stroke="#FFEDD5" stroke-width="0.8"/>
                    <line x1="7.5" y1="17.5" x2="16.5" y2="17.5" stroke="#FFEDD5" stroke-width="0.8"/>
                    <line x1="7.5" y1="20.5" x2="16.5" y2="20.5" stroke="#FFEDD5" stroke-width="0.8"/>
                    <rect x="7" y="1.5" width="10" height="5.8" rx="1.5" fill="#C2410C"/>
                    <rect x="8.5" y="2.5" width="7" height="2" rx="0.5" fill="#FEF08A"/>
                    <rect x="5.2" y="3" width="1.5" height="1" rx="0.3" fill="#C2410C"/>
                    <rect x="17.3" y="3" width="1.5" height="1" rx="0.3" fill="#C2410C"/>
                </svg>
            `}get_hub_icon_svg(e){return e==="Ocean"||e==="seaport"||e==="port"?`
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#0055B3" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="5" r="3"/>
                    <line x1="12" y1="22" x2="12" y2="8"/>
                    <path d="M5 12H2a10 10 0 0 0 20 0h-3"/>
                </svg>
            `:`
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#007AFF" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.2-1.1.6L2.5 8l6.4 3.3L7 15l-3.3-1.1-1.2 1.3 4.2 3.8 3.8 4.2 1.3-1.2L10.7 18.7l3.7-1.9 3.3 6.4 1.2-1.2-.4-2.6Z"/>
                </svg>
            `}get_active_vehicle_mode(e,t){if(!e)return"Ocean";let n=e.shipping_method||"Ocean",i=(e.status||"").toLowerCase();if(["delivered","completed","received","closed","giao h\xE0ng th\xE0nh c\xF4ng","giao h\xE0ng","nh\u1EADp kho","chu\u1EA9n b\u1ECB nh\u1EADp kho"].some(d=>i.includes(d))||["customs clearance","customs","th\xF4ng quan","h\u1EA3i quan","ch\u1EDD nh\u1EADp kho"].some(d=>i.includes(d)))return"Road";if(e.transit_route&&Array.isArray(e.transit_route)){let d=e.transit_route.find(o=>o.is_current==1||o.activity&&o.activity.includes("(Current Position)"));if(d){let o=(d.milestone||"").toUpperCase();if(["ARRIVED","DISCHARGED","GATE_OUT","DELIVERED"].includes(o)||["BOOKED","GATE_IN"].includes(o))return"Road"}}let a=typeof t=="number"?t:typeof e.progress=="number"?e.progress:.55,s=e.progress_thresholds||[0,.05,.95,1],l=s[1]!==void 0?s[1]:.05,c=s[2]!==void 0?s[2]:.95;return a<=l||a>=c?"Road":n==="Air"?"Air":"Ocean"}calculateBearing(e,t,n,i){let a=Math.PI/180,s=180/Math.PI,l=e*a,c=n*a,d=(i-t)*a;for(;d>Math.PI;)d-=2*Math.PI;for(;d<-Math.PI;)d+=2*Math.PI;let o=Math.sin(d)*Math.cos(c),r=Math.cos(l)*Math.sin(c)-Math.sin(l)*Math.cos(c)*Math.cos(d);return(Math.atan2(o,r)*s+360)%360}computePolylineMetrics(e){let t=[0],n=0;if(!e||e.length<=1)return{cumulative:[0],total:0};for(let i=0;i<e.length-1;i++){let[a,s]=e[i],[l,c]=e[i+1],d=c-s;d>180&&(d-=360),d<-180&&(d+=360);let o=l-a,r=Math.cos((a+l)/2*Math.PI/180);n+=Math.hypot(o,d*r),t.push(n)}return{cumulative:t,total:n}}interpolateAtProgress(e,t,n){if(!e||e.length===0)return{point:[0,0],bearing:0};if(e.length===1)return{point:e[0],bearing:0};let i=Math.max(0,Math.min(1,n));if(t.total===0)return{point:e[0],bearing:0};let a=i*t.total,s=0;for(let A=0;A<t.cumulative.length-1;A++)if(a>=t.cumulative[A]&&a<=t.cumulative[A+1]){s=A;break}s>=e.length-1&&(s=e.length-2);let l=t.cumulative[s],c=t.cumulative[s+1]-l,d=c===0?0:Math.max(0,Math.min(1,(a-l)/c)),o=e[s],r=e[s+1]||o,h=o[0]+d*(r[0]-o[0]),v=o[1],y=r[1]-v;y>180&&(y-=360),y<-180&&(y+=360);let C=v+d*y,S=this.calculateBearing(o[0],o[1],r[0],r[1]);return{point:[h,C],bearing:S}}perpendicularDistance(e,t,n){let[i,a]=e,[s,l]=t,[c,d]=n,o=d-l,r=c-s;o>180&&(o-=360),o<-180&&(o+=360);let h=a-l,v=i-s;h>180&&(h-=360),h<-180&&(h+=360);let f=o*o+r*r;if(f===0)return Math.hypot(h,v);let y=Math.max(0,Math.min(1,(h*o+v*r)/f)),C=y*o,S=y*r;return Math.hypot(h-C,v-S)}douglasPeucker(e,t=.002){if(!e||!Array.isArray(e)||e.length<=2)return e||[];let n=0,i=0,a=e.length-1;for(let s=1;s<a;s++){let l=this.perpendicularDistance(e[s],e[0],e[a]);l>n&&(n=l,i=s)}if(n>t){let s=this.douglasPeucker(e.slice(0,i+1),t),l=this.douglasPeucker(e.slice(i),t);return s.slice(0,s.length-1).concat(l)}else return[e[0],e[a]]}animateVehicle(e,t,n,i=1500,a="Ocean"){let s=this;if(this.currentAnimationId&&(cancelAnimationFrame(this.currentAnimationId),this.currentAnimationId=null),!e||!t||t.length===0)return;let l=this.computePolylineMetrics(t),c=typeof e._currentProgress=="number"?e._currentProgress:0,d=Math.max(0,Math.min(1,n)),o=performance.now();function r(h){let v=h-o,f=i<=0?1:Math.min(1,v/i),y=1-Math.pow(1-f,3),C=c+(d-c)*y,{point:S,bearing:A}=s.interpolateAtProgress(t,l,C);e.setLatLng(S);let g=e.getElement?e.getElement():null;if(g){if(e._shipment){let b=s.get_active_vehicle_mode(e._shipment,C);if(e._lastActiveMode!==b){e._lastActiveMode=b;let m=g.querySelector(".lw-vehicle-icon-svg");m&&(m.innerHTML=s.get_vehicle_svg(b));let T=g.querySelector(".lw-vehicle-box");T&&(T.style.borderColor=b==="Air"?"#007AFF":b==="Ocean"?"#0055B3":"#EA580C")}}let u=g.querySelector(".lw-vehicle-icon-svg")||g.querySelector("svg");u&&(u.style.transform=`rotate(${A}deg)`,u.style.transformOrigin="center center")}e._currentProgress=C,f<1?s.currentAnimationId=requestAnimationFrame(r):s.currentAnimationId=null}this.currentAnimationId=requestAnimationFrame(r)}update_map_view(e){!this.map||(e?this.render_single_shipment_map(e):this.render_fleet_overview_map(this.data?this.data.shipments||[]:[]))}align_route_coords(e,t=150){if(!e||!Array.isArray(e)||e.length===0)return e;let n=[],i=null,a=0;for(let o of e){if(!Array.isArray(o)||o.length<2||typeof o[1]!="number")continue;let r=o[0],h=o[1]+a;if(i!==null){let v=h-i;v>180?(a-=360,h-=360):v<-180&&(a+=360,h+=360)}i=h,n.push([r,h])}if(n.length===0)return e;let s=n.map(o=>o[1]),l=s.reduce((o,r)=>o+r,0)/s.length,c=0,d=Math.abs(l-t);for(let o of[-2,-1,1,2]){let r=Math.abs(l+o*360-t);r<d&&(d=r,c=o*360)}return c!==0?n.map(o=>[o[0],o[1]+c]):n}render_fleet_overview_map(e){if(!this.map)return;let t=window.L||window.leaflet;if(!t)return;let n=this;this.clear_map_layers(),$("#hub-map-title").text("B\u1EA3n \u0111\u1ED3 Gi\xE1m s\xE1t To\xE0n c\u1EA7u (Fleet Overview)"),$("#hub-map-reset-btn").addClass("active");let i=(e||[]).filter(c=>c.status==="In Transit"||c.status==="Customs Clearance");i.length===0&&(i=(e||[]).filter(c=>c.status!=="Draft")),i.length===0&&(i=e||[]),$("#hub-selected-shipment-badge").text(`To\xE0n c\u1EA3nh: ${i.length} l\xF4 h\xE0ng \u0111ang h\xE0nh tr\xECnh`).show(),this.update_marine_overlay("Ocean");let a=[],s={"san francisco":[37.619,-122.375],"tan son nhat":[10.8188,106.652],oakland:[37.804,-122.271],"hai phong":[20.865,106.683],"cat lai":[10.762,106.792],"long beach":[33.754,-118.216],"los angeles":[33.743,-118.267],shanghai:[31.23,121.473],singapore:[1.29,103.851],rotterdam:[51.924,4.477],busan:[35.179,129.075],tokyo:[35.676,139.65]};function l(c){if(!c)return null;let d=c.toLowerCase();for(let o in s)if(d.includes(o))return s[o];return null}if(i.forEach((c,d)=>{let o=c.shipping_method||"Ocean",r=o==="Air",h=o==="Road",v=[];if(c.full_route&&Array.isArray(c.full_route)&&c.full_route.length>=2?v=c.full_route:c.route&&Array.isArray(c.route)&&c.route.length>=2?v=c.route:c.legs&&Array.isArray(c.legs)&&c.legs.length>0&&c.legs.forEach(w=>{let k=w.coordinates_latlon||w.coordinates||[];k.length>0&&(v=v.concat(k))}),v.length<2){let w=l(c.origin_port)||[31.23,121.47],k=l(c.destination_port)||[10.76,106.79],D=w[1],H=k[1];D<0&&H>0&&Math.abs(D-H)>180?D+=360:H<0&&D>0&&Math.abs(H-D)>180&&(H+=360);let O=(w[0]+k[0])/2+(r?6:-3),R=(D+H)/2;v=[[w[0],D],[O,R],[k[0],H]]}v=n.align_route_coords(v,150);let f=n.douglasPeucker(v,.003);if((!f||f.length<2)&&(f=v),c.legs&&Array.isArray(c.legs)&&c.legs.length>0)c.legs.forEach(w=>{let k=w.coordinates_latlon||w.coordinates||[];if(k.length>=2){k=n.align_route_coords(k,150);let D=n.douglasPeucker(k,.003);(!D||D.length<2)&&(D=k);let H=w.mode||(w.vehicle_type==="Truck"?"Road":o),O=H==="Road",R=H==="Air",P=O?"#FF9500":R?"#0284c7":"#0055B3";c.is_delayed==1&&!O&&(P="#DC2626");let N=t.polyline(D,{color:P,weight:O?3:3.8,opacity:.85,dashArray:R||O?"6, 8":""}).addTo(n.map);N.bindTooltip(`<b>${c.name}</b> (${c.carrier||""})<br>${w.name||"H\xE0nh tr\xECnh"}<br><span style="color:#0071E3; font-weight:600;">\u{1F449} Nh\u1EA5p \u0111\u1EC3 xem \u0111\u01A1n n\xE0y</span>`,{sticky:!0}),N.on("click",()=>{n.select_shipment(c.name)}),n.mapLayers.routePolylines.push(N),a.push(N)}});else{let w=h?"#FF9500":r?"#0284c7":"#0055B3";c.is_delayed==1&&(w="#DC2626");let k=t.polyline(f,{color:w,weight:3.5,opacity:.82,dashArray:r||h?"6, 8":""}).addTo(n.map);k.bindTooltip(`<b>${c.name}</b> (${c.carrier||""})<br>${c.origin_port||"Origin"} \u2794 ${c.destination_port||"Dest"}<br><span style="color:#0071E3; font-weight:600;">\u{1F449} Nh\u1EA5p \u0111\u1EC3 xem \u0111\u01A1n n\xE0y</span>`,{sticky:!0}),k.on("click",()=>{n.select_shipment(c.name)}),n.mapLayers.routePolylines.push(k),a.push(k)}let C=f[0],S=f[f.length-1],A=c.origin&&c.origin.name||c.origin_port||c.name,g=t.circleMarker(C,{radius:5,color:"#16A34A",fillColor:"#FFFFFF",fillOpacity:1,weight:2}).addTo(n.map);g.bindTooltip(`Xu\u1EA5t ph\xE1t (Kho ngu\u1ED3n): ${A}`),g.on("click",()=>{n.select_shipment(c.name)}),n.mapLayers.markers.push(g);let u=c.destination&&c.destination.name||"Kho b\xE3i Logistics C\xE1p Kim Kh\xE1nh \u0110\xE0 N\u1EB5ng",b=t.circleMarker(S,{radius:5,color:"#DC2626",fillColor:"#FFFFFF",fillOpacity:1,weight:2}).addTo(n.map);b.bindTooltip(`\u0110\xEDch \u0111\u1EBFn: ${u}`),b.on("click",()=>{n.select_shipment(c.name)}),n.mapLayers.markers.push(b);let m=typeof c.progress=="number"?c.progress:.55,T=n.get_active_vehicle_mode(c,m),E=n.computePolylineMetrics(f),_=n.interpolateAtProgress(f,E,m),x=c.is_delayed==1?"#DC2626":T==="Air"?"#007AFF":T==="Ocean"?"#0055B3":"#EA580C",L=t.divIcon({className:"custom-fleet-vehicle-icon",html:`
                    <div style="background: white; border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; box-shadow: 0 3px 8px rgba(0,0,0,0.3); border: 2.5px solid ${x}; cursor: pointer; transition: transform 0.2s;" title="${c.name} - ${c.carrier||""}">
                        <div style="display: flex; align-items: center; justify-content: center; transform: rotate(${_.bearing}deg); transform-origin: center center;">
                            ${n.get_vehicle_svg(T)}
                        </div>
                    </div>
                `,iconSize:[36,36],iconAnchor:[18,18]}),I=t.marker(_.point,{icon:L,zIndexOffset:500+d*10}).addTo(n.map),M=T==="Air"?"H\xE0ng kh\xF4ng (M\xE1y bay \u2708\uFE0F)":T==="Ocean"?"\u0110\u01B0\u1EDDng bi\u1EC3n (T\xE0u h\xE0ng \u{1F6A2})":"\u0110\u01B0\u1EDDng b\u1ED9 (Xe t\u1EA3i \u{1F69A})";I.bindTooltip(`
                <div style="font-size: 11.5px; line-height: 1.4;">
                    <strong style="color: #0071E3;">${c.name}</strong> (${c.carrier||""})<br>
                    ${c.origin?c.origin.name:c.origin_port||"Origin"} \u2794 ${c.destination?c.destination.name:"Kho b\xE3i Logistics C\xE1p Kim Kh\xE1nh \u0110\xE0 N\u1EB5ng"}<br>
                    Ph\u01B0\u01A1ng ti\u1EC7n hi\u1EC7n t\u1EA1i: <b>${M}</b><br>
                    Tr\u1EA1ng th\xE1i: <b>${c.status}</b><br>
                    <span style="color: #0071E3; font-weight: 600;">\u{1F449} Nh\u1EA5p \u0111\u1EC3 xem h\xE0nh tr\xECnh chi ti\u1EBFt</span>
                </div>
            `,{direction:"top",offset:[0,-12]}),I.on("click",()=>{n.select_shipment(c.name)}),n.mapLayers.fleetVehicleMarkers.push(I),a.push(I)}),a.length>0)try{let d=t.featureGroup(a).getBounds(),o=n.map.getBoundsZoom(d,!1,[50,50]);n.map.setView(d.getCenter(),Math.min(Math.max(o,2),3))}catch(c){n.map.setView([22,150],3)}else n.map.setView([22,150],3)}render_single_shipment_map(e){if(!this.map||!e)return;let t=window.L||window.leaflet;if(!t)return;this.clear_map_layers(),$("#hub-map-title").text(`H\xE0nh tr\xECnh Chi ti\u1EBFt: ${e.name}`),$("#hub-map-reset-btn").removeClass("active"),$("#hub-selected-shipment-badge").text(`L\xF4 h\xE0ng: ${e.name} (${e.carrier||""})`).show();let n=e.shipping_method||"Ocean";this.update_marine_overlay(n);let i=[];if(e.full_route&&Array.isArray(e.full_route)&&e.full_route.length>0?i=e.full_route:e.route&&Array.isArray(e.route)&&e.route.length>0?i=e.route:e.legs&&Array.isArray(e.legs)&&e.legs.length>0&&e.legs.forEach(_=>{let x=_.coordinates_latlon||_.coordinates||[];x.length>0&&(i=i.concat(x))}),i.length===0){let _=parseFloat(e.current_lat)||20,x=parseFloat(e.current_lon)||120;i=[[31.23,121.47],[_,x],[10.77,106.7]]}i=this.align_route_coords(i,150);let a=this.douglasPeucker(i,.002);(!a||a.length<2)&&(a=i);let s=[];if(e.legs&&Array.isArray(e.legs)&&e.legs.length>0&&e.legs.forEach(_=>{let x=_.coordinates_latlon||_.coordinates||[];if(x.length>=2){x=this.align_route_coords(x,150);let L=this.douglasPeucker(x,.002);(!L||L.length<2)&&(L=x);let I=_.mode==="Road",M=_.mode==="Air",w=I?"#FF9500":M?"#0284c7":"#0055B3",k=I||M?"6, 8":"",D=I?3.5:4,H=t.polyline(L,{color:w,weight:D,opacity:.9,dashArray:k}).addTo(this.map);s.push(H),this.mapLayers.routePolylines.push(H)}}),s.length===0){let _=n==="Air",x=n==="Road",L=t.polyline(a,{color:x?"#FF9500":_?"#0284c7":"#0055B3",weight:4,opacity:.9,dashArray:_||x?"6, 8":""}).addTo(this.map);s.push(L),this.mapLayers.routePolylines.push(L)}let l=a[0],c=e.origin&&e.origin.name||e.origin_port||"Kho/Nh\xE0 m\xE1y xu\u1EA5t ph\xE1t",d=t.divIcon({className:"hub-origin-marker-icon",html:'<div style="background: #16a34a; color: white; border-radius: 50%; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 800; border: 2.5px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.3); cursor: pointer;" title="\u0110i\u1EC3m xu\u1EA5t ph\xE1t (Kho ngu\u1ED3n - \u0110i\u1EC3m O)">O</div>',iconSize:[26,26],iconAnchor:[13,13]}),o=t.marker(l,{icon:d}).addTo(this.map),r=((l[1]+180)%360+360)%360-180;o.bindPopup(`<b>\u0110i\u1EC3m xu\u1EA5t ph\xE1t (Kho ngu\u1ED3n):</b><br>${c}<br><small>To\u1EA1 \u0111\u1ED9: ${l[0].toFixed(4)}, ${r.toFixed(4)}</small>`),this.mapLayers.markers.push(o);let h=a[a.length-1],v=e.destination&&e.destination.name||"Kho b\xE3i Logistics C\xE1p Kim Kh\xE1nh \u0110\xE0 N\u1EB5ng (G\u1EA7n \u0110H B\xE1ch Khoa)",f=t.divIcon({className:"hub-dest-marker-icon",html:'<div style="background: #dc2626; color: white; border-radius: 50%; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 800; border: 2.5px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.3); cursor: pointer;" title="\u0110i\u1EC3m \u0111\xEDch \u0111\u1EBFn (Kho C\xE1p Kim Kh\xE1nh \u0110\xE0 N\u1EB5ng - \u0110i\u1EC3m D)">D</div>',iconSize:[26,26],iconAnchor:[13,13]}),y=t.marker(h,{icon:f}).addTo(this.map),C=((h[1]+180)%360+360)%360-180;if(y.bindPopup(`<b>\u0110i\u1EC3m \u0111\xEDch \u0111\u1EBFn (Kho nh\u1EADn h\xE0ng):</b><br>${v}<br><small>To\u1EA1 \u0111\u1ED9: ${h[0].toFixed(4)}, ${C.toFixed(4)}</small>`),this.mapLayers.markers.push(y),e.legs&&e.legs.length>=2){let _=e.legs[0],x=e.legs[1],L=_.coordinates_latlon&&_.coordinates_latlon.length>0?_.coordinates_latlon[_.coordinates_latlon.length-1]:null,I=x.coordinates_latlon&&x.coordinates_latlon.length>0?x.coordinates_latlon[x.coordinates_latlon.length-1]:null;if(L){let M=t.divIcon({className:"hub-dep-port-icon",html:`<div style="background: white; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border: 2.5px solid #0055B3; box-shadow: 0 2px 5px rgba(0,0,0,0.25); cursor: pointer;" title="C\u1EA3ng/S\xE2n bay xu\u1EA5t ph\xE1t">
                        ${this.get_hub_icon_svg(n)}
                    </div>`,iconSize:[28,28],iconAnchor:[14,14]}),w=t.marker(L,{icon:M}).addTo(this.map);w.bindPopup(`<b>Tr\u1EA1m trung chuy\u1EC3n xu\u1EA5t:</b><br>${e.origin_port||"C\u1EA3ng/S\xE2n bay xu\u1EA5t"}`),this.mapLayers.markers.push(w)}if(I){let M=t.divIcon({className:"hub-arr-port-icon",html:`<div style="background: white; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; border: 2.5px solid #0055B3; box-shadow: 0 2px 5px rgba(0,0,0,0.25); cursor: pointer;" title="C\u1EA3ng/S\xE2n bay \u0111\u1EBFn">
                        ${this.get_hub_icon_svg(n)}
                    </div>`,iconSize:[28,28],iconAnchor:[14,14]}),w=t.marker(I,{icon:M}).addTo(this.map);w.bindPopup(`<b>Tr\u1EA1m trung chuy\u1EC3n \u0111\u1EBFn:</b><br>${e.destination_port||"C\u1EA3ng/S\xE2n bay \u0111\u1EBFn"}`),this.mapLayers.markers.push(w)}}let S=typeof e.progress=="number"?e.progress:.55,A=this.get_active_vehicle_mode(e,S),g=this.computePolylineMetrics(a),u=this.interpolateAtProgress(a,g,0),b=A==="Air"?"#007AFF":A==="Ocean"?"#0055B3":"#EA580C",m=t.divIcon({className:"custom-vehicle-icon-hub",html:`
                <div class="lw-vehicle-box" style="background: white; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; box-shadow: 0 3px 10px rgba(0,0,0,0.3); border: 2.8px solid ${b};">
                    <div class="lw-vehicle-icon-svg" style="display: flex; align-items: center; justify-content: center; transform: rotate(${u.bearing}deg); transform-origin: center center;">
                        ${this.get_vehicle_svg(A)}
                    </div>
                </div>
            `,iconSize:[40,40],iconAnchor:[20,20]});this.mapLayers.vehicleMarker=t.marker(u.point,{icon:m,zIndexOffset:1e3}).addTo(this.map),this.mapLayers.vehicleMarker._currentProgress=0,this.mapLayers.vehicleMarker._shipment=e,this.mapLayers.vehicleMarker._lastActiveMode=A;let T=e.delay_days>0?`<div style="color: #dc2626; font-weight: 700; margin-top: 4px;">\u26A0\uFE0F L\u1EC7ch ETA: +${e.delay_days} ng\xE0y</div>`:'<div style="color: #16a34a; font-weight: 600; margin-top: 4px;">\u2705 H\xE0nh tr\xECnh \u0111\xFAng ti\u1EBFn \u0111\u1ED9</div>',E=A==="Air"?"H\xE0ng kh\xF4ng (M\xE1y bay \u2708\uFE0F)":A==="Ocean"?"\u0110\u01B0\u1EDDng bi\u1EC3n (T\xE0u h\xE0ng \u{1F6A2})":"\u0110\u01B0\u1EDDng b\u1ED9 (Xe t\u1EA3i \u{1F69A})";this.mapLayers.vehicleMarker.bindPopup(`
            <div style="font-size: 12px; min-width: 190px; line-height: 1.5;">
                <div style="font-weight: 700; color: #0284c7; font-size: 13px; border-bottom: 1px solid #e2e8f0; padding-bottom: 3px; margin-bottom: 4px;">
                    ${e.name}
                </div>
                <div><b>Ph\u01B0\u01A1ng ti\u1EC7n hi\u1EC7n t\u1EA1i:</b> ${E}</div>
                <div><b>\u0110\u01A1n v\u1ECB v\u1EADn chuy\u1EC3n:</b> ${e.carrier||""} (${e.vessel_name||e.flight_number||"V\u1EADn t\u1EA3i \u0111a ph\u01B0\u01A1ng th\u1EE9c"})</div>
                <div><b>M\xE3 Container:</b> ${e.container_id||"N/A"}</div>
                <div><b>Tr\u1EA1ng th\xE1i:</b> ${e.status}</div>
                <div><b>L\u1ED9 tr\xECnh:</b> ${e.origin?e.origin.name:e.origin_port||"Origin"} \u2794 ${e.destination?e.destination.name:"Kho b\xE3i Logistics C\xE1p Kim Kh\xE1nh \u0110\xE0 N\u1EB5ng"}</div>
                ${T}
            </div>
        `),this.animateVehicle(this.mapLayers.vehicleMarker,a,S,1600);try{let x=t.featureGroup(s).getBounds(),L=this.map.getBoundsZoom(x,!1,[45,45]);this.map.setView(x.getCenter(),Math.min(Math.max(L,2),7))}catch(_){this.map.setView(u.point,4)}}clear_map_layers(){if(!!this.map){if(this.currentAnimationId&&(cancelAnimationFrame(this.currentAnimationId),this.currentAnimationId=null),this.mapLayers.routePolylines.forEach(e=>{try{this.map.removeLayer(e)}catch(t){}}),this.mapLayers.routePolylines=[],this.mapLayers.markers.forEach(e=>{try{this.map.removeLayer(e)}catch(t){}}),this.mapLayers.markers=[],this.mapLayers.vehicleMarker){try{this.map.removeLayer(this.mapLayers.vehicleMarker)}catch(e){}this.mapLayers.vehicleMarker=null}this.mapLayers.fleetVehicleMarkers&&(this.mapLayers.fleetVehicleMarkers.forEach(e=>{try{this.map.removeLayer(e)}catch(t){}}),this.mapLayers.fleetVehicleMarkers=[])}}reset_map_view(){this.selectedShipment=null,$("#hub-shipments-tbody tr").removeClass("selected"),this.render_stepper(null),this.render_fleet_overview_map(this.data?this.data.shipments||[]:[])}sync_now(e){let t=this,n=$("#hub-btn-sync-now");n.prop("disabled",!0).html('<i class="fa fa-spinner fa-spin"></i> \u0110ang \u0111\u1ED3ng b\u1ED9...'),frappe.call({method:"logistics_wizard.api.sync_shipment_now",args:{shipment:e},callback:function(i){n.prop("disabled",!1).html('<i class="fa fa-cloud-download"></i> \u0110\u1ED3ng b\u1ED9 t\u1EE9c th\xEC (Sync Now)'),i&&i.message&&i.message.success!==!1?(frappe.show_alert({message:__("\u0110\u1ED3ng b\u1ED9 h\xE0nh tr\xECnh th\xE0nh c\xF4ng!"),indicator:"green"}),t.refresh(e)):(frappe.msgprint({title:__("\u0110\u1ED3ng b\u1ED9 ho\xE0n t\u1EA5t"),message:i.message?i.message.message:__("\u0110\xE3 ki\u1EC3m tra d\u1EEF li\u1EC7u h\xE0nh tr\xECnh m\u1EDBi nh\u1EA5t."),indicator:"blue"}),t.refresh(e))},error:function(){n.prop("disabled",!1).html('<i class="fa fa-cloud-download"></i> \u0110\u1ED3ng b\u1ED9 t\u1EE9c th\xEC (Sync Now)'),frappe.show_alert({message:__("L\u1ED7i k\u1EBFt n\u1ED1i khi \u0111\u1ED3ng b\u1ED9!"),indicator:"red"})}})}},K=class{constructor(e){this.wrapper=e,this.currentCaseId="",this.currentRule="weight",this.currentCaseType="all",this.caseData=this.get_mock_cases_data()}init(){this.bind_events(),this.load_data("")}get_mock_cases_data(){return{"IMP-2026-001":{case_id:"IMP-2026-001",party:"ABC Electronics Co., Ltd",case_type:"import",po_value:125e3,estimated_cost:16800,actual_cost:18350,variance_amount:1550,variance_pct:9.2,status:"\u0110ang \u0110\u1ED1i So\xE1t",status_class:"badge-in-transit",lcv_id:"LCV-2026-0004",cost_items:[{type:"C\u01B0\u1EDBc v\u1EADn chuy\u1EC3n bi\u1EC3n (Ocean Freight)",supplier:"Maersk Line Vietnam",inv_no:"INV-MAE-8821",est:8500,act:9200,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"B\u1EA3o hi\u1EC3m h\xE0ng h\xF3a (Cargo Insurance)",supplier:"Bao Viet Insurance",inv_no:"BV-2026-091",est:600,act:650,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Thu\u1EBF nh\u1EADp kh\u1EA9u (Customs Import Duty)",supplier:"Chi c\u1EE5c H\u1EA3i Quan C\u1EA3ng SG KV4",inv_no:"HQ-77218-TK",est:3200,act:3200,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Thu\u1EBF GTGT h\xE0ng nh\u1EADp kh\u1EA9u (Import VAT)",supplier:"Chi c\u1EE5c H\u1EA3i Quan C\u1EA3ng SG KV4",inv_no:"HQ-77218-VAT",est:1500,act:1500,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Ph\xED THC & ph\u1EE5 ph\xED c\u1EA3ng (Port Surcharges)",supplier:"T\xE2n C\u1EA3ng S\xE0i G\xF2n (SNP)",inv_no:"SNP-2026-112",est:850,act:950,status:"\u0110ang \u0110\u1ED1i So\xE1t"},{type:"N\xE2ng h\u1EA1 & l\u01B0u kho (Handling & Storage)",supplier:"C\u1EA3ng C\xE1t L\xE1i ICD",inv_no:"ICD-44120",est:400,act:580,status:"\u0110ang \u0110\u1ED1i So\xE1t"},{type:"L\u01B0u b\xE3i container (Demurrage/Detention)",supplier:"Maersk Line Vietnam",inv_no:"DEM-8821-02",est:0,act:320,status:"C\u1EA7n R\xE0 So\xE1t"},{type:"V\u1EADn chuy\u1EC3n n\u1ED9i \u0111\u1ECBa (Trucking)",supplier:"Huu Toan Logistics",inv_no:"HT-9901-TRK",est:950,act:1100,status:"\u0110ang \u0110\u1ED1i So\xE1t"},{type:"Ph\xED d\u1ECBch v\u1EE5 h\u1EA3i quan (Customs Brokerage)",supplier:"Schenker Vietnam",inv_no:"DB-8812-FEE",est:500,act:500,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Ki\u1EC3m tra ch\u1EA5t l\u01B0\u1EE3ng (Inspection)",supplier:"Quatest 3",inv_no:"QT3-11029",est:300,act:350,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Chi ph\xED ph\u1EE5 kh\xE1c (Other Contingency)",supplier:"N\u1ED9i b\u1ED9 c\xF4ng ty",inv_no:"INT-EXP-01",est:0,act:0,status:"Ch\u1EDD H\xF3a \u0110\u01A1n"}],items_to_allocate:[{item_code:"CPU-INTEL-I9",name:"Intel Core i9-14900K Processor",qty:200,unit_price:350,weight:.15,volume:4e-4},{item_code:"RAM-DDR5-32G",name:"Corsair Vengeance 32GB DDR5 RAM",qty:500,unit_price:70,weight:.08,volume:2e-4},{item_code:"SSD-NVME-2TB",name:"Samsung 990 Pro 2TB NVMe SSD",qty:200,unit_price:100,weight:.06,volume:15e-5}],audit_checks:[{title:"Tr\xF9ng L\u1EB7p H\xF3a \u0110\u01A1n (Duplicate Check)",status:"H\u1EE3p l\u1EC7",status_class:"delay-tag-ontime",border:"#10b981",desc:"Kh\xF4ng ph\xE1t hi\u1EC7n h\xF3a \u0111\u01A1n tr\xF9ng l\u1EB7p s\u1ED1 ch\u1EE9ng t\u1EEB ho\u1EB7c nh\xE0 cung c\u1EA5p."},{title:"Chi Ph\xED Tr\u1ECDng Y\u1EBFu (Missing Cost Check)",status:"C\u1EA7n r\xE0 so\xE1t",status_class:"delay-tag-positive",border:"#d97706",desc:"Ch\u01B0a nh\u1EADn h\xF3a \u0111\u01A1n n\xE2ng h\u1EA1 c\u1EA3ng \u0111\xEDch (Port Handling D/O). C\u1EA7n li\xEAn h\u1EC7 \u0111\u1EA1i l\xFD h\xE3ng t\xE0u tr\u01B0\u1EDBc ng\xE0y 14/10."},{title:"G\xE1n \u0110\xFAng V\u1EE5 Vi\u1EC7c (Association Check)",status:"Kh\u1EDBp 100%",status_class:"delay-tag-ontime",border:"#10b981",desc:"T\u1EA5t c\u1EA3 6 h\xF3a \u0111\u01A1n d\u1ECBch v\u1EE5 \u0111\u1EC1u tham chi\u1EBFu ch\xEDnh x\xE1c s\u1ED1 PO-2026-0042 v\xE0 Trade Case IMP-2026-001."}]},"EXP-2026-002":{case_id:"EXP-2026-002",party:"Global Coffee Exporter JSC",case_type:"export",po_value:65e3,estimated_cost:3800,actual_cost:4200,variance_amount:400,variance_pct:10.5,status:"S\u1EB5n S\xE0ng Xu\u1EA5t Kh\u1EA9u",status_class:"badge-delivered",lcv_id:"LCV-2026-EXP-01",export_revenue:65e3,export_cogs:45e3,export_logistics:4200,cost_items:[{type:"C\u01B0\u1EDBc v\u1EADn chuy\u1EC3n bi\u1EC3n xu\u1EA5t (Ocean Freight Export)",supplier:"ONE Ocean Network Express",inv_no:"ONE-EX-3312",est:2200,act:2450,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"B\u1EA3o hi\u1EC3m h\xE0ng h\xF3a (Marine Cargo Insurance)",supplier:"Bao Minh Insurance",inv_no:"BM-2026-339",est:250,act:270,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Thu\u1EBF xu\u1EA5t kh\u1EA9u (Export Duty)",supplier:"H\u1EA3i Quan C\u1EA3ng Quy Nh\u01A1n",inv_no:"HQ-EXP-0081",est:0,act:0,status:"Mi\u1EC5n Thu\u1EBF"},{type:"Ph\xED THC c\u1EA3ng b\u1ED1c (Port Handling Surcharge)",supplier:"C\u1EA3ng Qu\u1ED1c T\u1EBF Quy Nh\u01A1n",inv_no:"QN-THC-881",est:350,act:380,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Hun tr\xF9ng & Ki\u1EC3m d\u1ECBch (Fumigation & Phytosanitary)",supplier:"VFC Fumigation Co.",inv_no:"VFC-2026-77",est:180,act:180,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"L\xE0m th\u1EE7 t\u1EE5c C/O Form ICO (Certificate of Origin)",supplier:"VCCI Chi nh\xE1nh \u0110\xE0 N\u1EB5ng",inv_no:"VCCI-CO-102",est:70,act:70,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"K\xE9o v\u1ECF & v\u1EADn chuy\u1EC3n n\u1ED9i \u0111\u1ECBa (Trucking)",supplier:"Binh Dinh Express Logistics",inv_no:"BD-TRK-551",est:500,act:580,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Ph\xED m\xF4i gi\u1EDBi h\u1EA3i quan (Brokerage Fee)",supplier:"Transimex Logistics",inv_no:"TMX-2026-44",est:150,act:170,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Chi ph\xED ph\u1EE5 kh\xE1c (Contingency)",supplier:"N\u1ED9i b\u1ED9",inv_no:"INT-EXP-02",est:100,act:100,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"}],items_to_allocate:[{item_code:"COFFEE-ROBUSTA-G1",name:"Robusta Green Coffee Beans Grade 1",qty:2e4,unit_price:2.25,weight:1,volume:.0015},{item_code:"COFFEE-ARABICA-S18",name:"Arabica Roasted Coffee Screen 18",qty:5e3,unit_price:4,weight:1,volume:.0018}],audit_checks:[{title:"Tr\xF9ng L\u1EB7p H\xF3a \u0110\u01A1n (Duplicate Check)",status:"H\u1EE3p l\u1EC7",status_class:"delay-tag-ontime",border:"#10b981",desc:"Kh\xF4ng c\xF3 ch\u1EE9ng t\u1EEB tr\xF9ng l\u1EB7p \u0111\u1ED1i t\xE1c xu\u1EA5t kh\u1EA9u."},{title:"Chi Ph\xED Tr\u1ECDng Y\u1EBFu (Missing Cost Check)",status:"\u0110\u1EA7y \u0111\u1EE7",status_class:"delay-tag-ontime",border:"#10b981",desc:"\u0110\xE3 nh\u1EADn \u0111\u1EE7 ch\u1EE9ng t\u1EEB hun tr\xF9ng, C/O v\xE0 bill of lading."},{title:"G\xE1n \u0110\xFAng V\u1EE5 Vi\u1EC7c (Association Check)",status:"Kh\u1EDBp 100%",status_class:"delay-tag-ontime",border:"#10b981",desc:"H\xF3a \u0111\u01A1n ONE v\xE0 VFC tham chi\u1EBFu ch\xEDnh x\xE1c Sales Order SO-2026-009."}]},"IMP-2026-003":{case_id:"IMP-2026-003",party:"Pacific Seafood Import Co.",case_type:"import",po_value:84e3,estimated_cost:11200,actual_cost:11050,variance_amount:-150,variance_pct:-1.3,status:"\u0110\xE3 Ho\xE0n T\u1EA5t",status_class:"badge-delivered",lcv_id:"LCV-2026-0002",cost_items:[{type:"C\u01B0\u1EDBc v\u1EADn chuy\u1EC3n h\xE0ng \u0111\xF4ng l\u1EA1nh (Reefer Freight)",supplier:"Hapag-Lloyd Vietnam",inv_no:"HL-RF-9021",est:6800,act:6700,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"B\u1EA3o hi\u1EC3m h\xE0ng h\xF3a (Reefer Cargo Insurance)",supplier:"PVI Insurance",inv_no:"PVI-RF-122",est:450,act:450,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Thu\u1EBF nh\u1EADp kh\u1EA9u (Customs Import Duty)",supplier:"Chi c\u1EE5c H\u1EA3i Quan C\u1EA3ng H\u1EA3i Ph\xF2ng",inv_no:"HQ-HP-3312",est:1800,act:1800,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"Ki\u1EC3m d\u1ECBch th\u1EE7y s\u1EA3n (Fisheries Quarantine)",supplier:"Chi c\u1EE5c Th\xFA Y V\xF9ng 2",inv_no:"KD-HP-0091",est:350,act:350,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"C\u1EAFm \u0111i\u1EC7n container l\u1EA1nh (Reefer Monitoring)",supplier:"C\u1EA3ng Qu\u1ED1c T\u1EBF L\u1EA1ch Huy\u1EC7n",inv_no:"LH-REEFER-11",est:500,act:450,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"},{type:"V\u1EADn chuy\u1EC3n xe l\u1EA1nh n\u1ED9i \u0111\u1ECBa (Reefer Trucking)",supplier:"Vinalines Cold Chain",inv_no:"VNL-COLD-88",est:1300,act:1300,status:"\u0110\xE3 \u0110\u1ED1i So\xE1t"}],items_to_allocate:[{item_code:"SEAFOOD-SALMON-NOR",name:"Fresh Norwegian Salmon Fillet",qty:4e3,unit_price:15,weight:1,volume:.0016},{item_code:"SEAFOOD-COD-ATL",name:"Atlantic Cod Fillet Frozen",qty:2e3,unit_price:12,weight:1,volume:.0015}],audit_checks:[{title:"Tr\xF9ng L\u1EB7p H\xF3a \u0110\u01A1n (Duplicate Check)",status:"H\u1EE3p l\u1EC7",status_class:"delay-tag-ontime",border:"#10b981",desc:"Kh\xF4ng ph\xE1t hi\u1EC7n tr\xF9ng s\u1ED1 h\xF3a \u0111\u01A1n."},{title:"Chi Ph\xED Tr\u1ECDng Y\u1EBFu (Missing Cost Check)",status:"\u0110\u1EA7y \u0111\u1EE7",status_class:"delay-tag-ontime",border:"#10b981",desc:"\u0110\u1EA7y \u0111\u1EE7 ph\xED c\u1EAFm \u0111i\u1EC7n kho l\u1EA1nh v\xE0 ki\u1EC3m d\u1ECBch th\xFA y."},{title:"G\xE1n \u0110\xFAng V\u1EE5 Vi\u1EC7c (Association Check)",status:"Kh\u1EDBp 100%",status_class:"delay-tag-ontime",border:"#10b981",desc:"Ch\u1EE9ng t\u1EEB L\u1EA1ch Huy\u1EC7n kh\u1EDBp 100% h\u1ED3 s\u01A1 h\u1EA3i quan."}]}}}load_data(e,t){let n=this,i=e!==void 0?e:this.currentCaseId||"",a=t!==void 0?t:this.currentCaseType==="all"?"":this.currentCaseType;typeof frappe!="undefined"&&frappe.call?frappe.call({method:"logistics_wizard.costing_engine.api.get_cost_dashboard_data",args:{case_id:i||void 0,trade_type_filter:a||void 0},callback:function(s){let l=s&&s.message;l&&l.success?(n.liveData=l,n.currentCaseId=l.case_id||i,n.populate_case_selector(l.available_cases||[],n.currentCaseId),n.render_dashboard()):(n.liveData=null,n.currentCaseId=i||"",$("#tcd-case-selector").val(n.currentCaseId),n.render_dashboard())},error:function(){n.liveData=null,n.currentCaseId=i||"",$("#tcd-case-selector").val(n.currentCaseId),n.render_dashboard()}}):(this.currentCaseId=i||Object.keys(this.caseData)[0]||"",$("#tcd-case-selector").val(this.currentCaseId),this.render_dashboard())}populate_case_selector(e,t){if(!e||!e.length)return;let n=$("#tcd-case-selector");if(!n.length)return;let i="";e.forEach(a=>{let s=a.case_id===t?" selected":"";i+=`<option value="${a.case_id}"${s}>${a.label||a.case_id}</option>`}),n.html(i),t&&n.val(t)}bind_events(){let e=this;$(document).on("change","#tcd-case-selector",function(){e.load_data($(this).val())}),$(document).on("click",".tcd-type-btn",function(){$(".tcd-type-btn").removeClass("active"),$(this).addClass("active"),e.currentCaseType=$(this).data("type"),e.apply_type_filter()}),$(document).on("click",".tcd-alloc-btn",function(){$(".tcd-alloc-btn").removeClass("active"),$(this).addClass("active"),e.currentRule=$(this).data("rule"),e.render_allocation_table()}),$(document).on("click","#tcd-btn-refresh",function(){let t=$(this).find("i");t.addClass("fa-spin"),e.load_data(e.currentCaseId),setTimeout(()=>{t.removeClass("fa-spin"),frappe.show_alert({message:__("\u0110\xE3 l\xE0m m\u1EDBi d\u1EEF li\u1EC7u Trade Cost t\u1EEB h\u1EC7 th\u1ED1ng!"),indicator:"green"})},400)}),$(document).on("click","#tcd-btn-new-sheet",function(){typeof frappe!="undefined"&&frappe.new_doc&&frappe.new_doc("Trade Cost Sheet",{trade_case:e.currentCaseId})}),$(document).on("click","#tcd-btn-sync-lcv, #tcd-btn-apply-lcv",function(){let t=e.get_active_case_data(),n=t&&t.cost_sheet_name;if(!n){frappe.msgprint({title:__("Ch\u01B0a c\xF3 Trade Cost Sheet"),message:__(`H\u1ED3 s\u01A1 <strong>${e.currentCaseId}</strong> ch\u01B0a c\xF3 b\u1EA3ng chi ph\xED (Trade Cost Sheet) \u0111\u1EC3 \u0111\u1ED3ng b\u1ED9 Landed Cost Voucher.`),indicator:"orange"});return}frappe.call({method:"logistics_wizard.costing_engine.api.allocate_and_sync_lcv",args:{cost_sheet_name:n,auto_submit:!1},callback:function(i){let a=i&&i.message?i.message:{};a.success?(frappe.show_alert({message:__(`\u0110\u1ED3ng b\u1ED9 Landed Cost Voucher th\xE0nh c\xF4ng: ${a.lcv_name||n}`),indicator:"green"}),e.load_data(e.currentCaseId)):frappe.msgprint({title:__("Kh\xF4ng th\u1EC3 \u0111\u1ED3ng b\u1ED9 LCV"),message:a.error||__("Vui l\xF2ng ki\u1EC3m tra Purchase Receipt v\xE0 c\xE1c d\xF2ng chi ph\xED tr\u01B0\u1EDBc khi \u0111\u1ED3ng b\u1ED9."),indicator:"red"})}})})}get_active_case_data(){return this.liveData&&this.liveData.success?this.liveData:this.caseData[this.currentCaseId]||this.caseData["IMP-2026-001"]}apply_type_filter(){let e=this.currentCaseType==="all"?"":this.currentCaseType;this.load_data("",e)}render_dashboard(){let e=this.get_active_case_data();if(!e)return;let t=Number(e.po_value||0),n=Number(e.estimated_cost||0),i=Number(e.actual_cost||0),a=Number(e.variance_amount||0),s=Number(e.variance_pct||0);$("#tcd-kpi-po-val").text("$"+t.toLocaleString("en-US",{minimumFractionDigits:2})),$("#tcd-kpi-est-val").text("$"+n.toLocaleString("en-US",{minimumFractionDigits:2})),$("#tcd-kpi-act-val").text("$"+i.toLocaleString("en-US",{minimumFractionDigits:2}));let l=a>0?"+":"",c=s>0?"+":"",d=`${l}$${a.toLocaleString("en-US",{minimumFractionDigits:2})} (${c}${s}%)`;$("#tcd-kpi-var-val").text(d),a>0?$("#tcd-kpi-var-val").css("color","#dc2626"):a<0?$("#tcd-kpi-var-val").css("color","#059669"):$("#tcd-kpi-var-val").css("color","#64748b"),$("#tcd-status-badge").attr("class","badge-status "+(e.status_class||"badge-in-transit")).text(e.status||"DRAFT"),$("#tcd-lcv-badge").text(e.lcv_id||"Ch\u01B0a li\xEAn k\u1EBFt"),this.render_cost_items(e.cost_items||[]),this.render_allocation_table(),this.render_audit_checks(e.audit_checks||[]),this.render_export_profitability(e)}render_export_profitability(e){var c,d,o,r,h,v,f,y,C,S;if((e.case_type||"").toLowerCase()!=="export"){$("#tcd-export-profitability-box").hide();return}let t=e.export_profitability||{},n=Number((o=(d=(c=t.export_revenue)!=null?c:e.export_revenue)!=null?d:e.po_value)!=null?o:0),i=Number((h=(r=t.export_cogs)!=null?r:e.export_cogs)!=null?h:0),a=Number((y=(f=(v=t.export_logistics_cost)!=null?v:e.export_logistics)!=null?f:e.actual_cost)!=null?y:0),s=Number((C=t.export_net_profit)!=null?C:n-i-a),l=Number((S=t.export_net_margin_pct)!=null?S:n>0?(s/n*100).toFixed(1):0);$("#tcd-export-profitability-box").html(`
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 12.5px; font-weight: 700; color: #0f172a;"><i class="fa fa-bar-chart" style="color: #059669;"></i> Hi\u1EC7u Qu\u1EA3 L\xF4 Xu\u1EA5t Kh\u1EA9u (Export Margin)</span>
                <span class="delay-tag-ontime">${l>=0?"+":""}${l}% Bi\xEAn L\u1EE3i Nhu\u1EADn</span>
            </div>
            <table class="table tc-table" style="margin-bottom: 0;">
                <tr><td class="label-col">Doanh thu xu\u1EA5t kh\u1EA9u:</td><td class="val-col text-right">$${n.toLocaleString("en-US",{minimumFractionDigits:2})}</td></tr>
                <tr><td class="label-col">Gi\xE1 v\u1ED1n h\xE0ng b\xE1n (COGS):</td><td class="val-col text-right">$${i.toLocaleString("en-US",{minimumFractionDigits:2})}</td></tr>
                <tr><td class="label-col">Chi ph\xED logistics xu\u1EA5t kh\u1EA9u:</td><td class="val-col text-right">$${a.toLocaleString("en-US",{minimumFractionDigits:2})}</td></tr>
                <tr style="border-top: 1px solid #e2e8f0; font-weight: 700;">
                    <td class="label-col" style="color: #059669;">L\u1EE3i nhu\u1EADn thu\u1EA7n th\u1EF1c t\u1EBF:</td>
                    <td class="val-col text-right" style="color: #059669; font-size: 13.5px;">$${s.toLocaleString("en-US",{minimumFractionDigits:2})}</td>
                </tr>
            </table>
        `).show()}render_cost_items(e){if(!e||!e.length){$("#tcd-cost-items-tbody").html('<tr><td colspan="7" class="text-center" style="color:#64748b; padding:16px;">Ch\u01B0a c\xF3 d\xF2ng chi ph\xED n\xE0o \u0111\u01B0\u1EE3c ghi nh\u1EADn cho h\u1ED3 s\u01A1 n\xE0y.</td></tr>');return}let t="";e.forEach(n=>{let i=Number(n.est||0),a=Number(n.act||0),s=a-i,l=s>0?"+":"",c=s>0?"tcd-var-positive":s<0?"tcd-var-negative":"tcd-var-zero";t+=`
                <tr>
                    <td style="font-weight: 600; color: #0f172a;">${n.type}</td>
                    <td style="color: #475569;">${n.supplier}</td>
                    <td><span style="font-family: monospace; font-size: 12px; color: #0369a1; background: #f0f9ff; padding: 2px 6px; border-radius: 4px; display: inline-block;">${n.inv_no}</span></td>
                    <td class="text-right" style="color: #64748b;">$${i.toLocaleString("en-US",{minimumFractionDigits:2})}</td>
                    <td class="text-right" style="font-weight: 600; color: #0f172a;">$${a.toLocaleString("en-US",{minimumFractionDigits:2})}</td>
                    <td class="text-right ${c}">${l}$${s.toLocaleString("en-US",{minimumFractionDigits:2})}</td>
                    <td class="text-center">
                        <span class="delay-tag-ontime" style="font-size: 11px;">${n.status}</span>
                    </td>
                </tr>
            `}),$("#tcd-cost-items-tbody").html(t)}render_allocation_table(){let e=this.get_active_case_data();if(!e||!e.items_to_allocate||!e.items_to_allocate.length){$("#tcd-allocation-tbody").html('<tr><td colspan="7" class="text-center" style="color:#64748b; padding:16px;">Ch\u01B0a c\xF3 danh m\u1EE5c h\xE0ng h\xF3a (PO/PR/SO) \u0111\u1EC3 m\xF4 ph\u1ECFng ph\xE2n b\u1ED5 Landed Cost.</td></tr>');return}let t=Number(e.actual_cost||0),n=this.calculate_allocation(e.items_to_allocate,t,this.currentRule),i="";n.forEach(a=>{i+=`
                <tr>
                    <td style="font-weight: 700; color: #0284c7;">${a.item_code}</td>
                    <td style="color: #334155;">${a.name}</td>
                    <td class="text-center" style="font-weight: 600;">${Number(a.qty||0).toLocaleString()}</td>
                    <td class="text-right">$${Number(a.unit_price||0).toFixed(2)}</td>
                    <td class="text-right" style="color: #0284c7; font-weight: 600;">+$${Number(a.allocated_cost||0).toFixed(2)}</td>
                    <td class="text-right" style="font-weight: 700; color: #059669;">$${Number(a.landed_unit_cost||0).toFixed(2)}</td>
                    <td class="text-center" style="color: #d97706; font-weight: 600;">+${a.pct_increase}%</td>
                </tr>
            `}),$("#tcd-allocation-tbody").html(i)}calculate_allocation(e,t,n){let i=[];n==="weight"?i=e.map(d=>d.weight*d.qty):n==="value"?i=e.map(d=>d.unit_price*d.qty):n==="qty"?i=e.map(d=>d.qty):n==="volume"&&(i=e.map(d=>d.volume*d.qty));let a=i.reduce((d,o)=>d+o,0)||1,s=[],l=0;for(let d=0;d<e.length;d++){let o=i[d]/a*t,r=Math.round(o*100)/100;s.push(r),l+=r}let c=Math.round((t-l)*100)/100;if(Math.abs(c)>1e-4&&s.length>0){let d=0;for(let o=1;o<s.length;o++)s[o]>s[d]&&(d=o);s[d]=Math.round((s[d]+c)*100)/100}return e.map((d,o)=>{let r=s[o],h=Math.round((d.unit_price+r/d.qty)*100)/100,v=d.unit_price*d.qty,f=v>0?(r/v*100).toFixed(1):0;return ee(Z({},d),{allocated_cost:r,landed_unit_cost:h,pct_increase:f})})}render_audit_checks(e){let t="";e.forEach(n=>{t+=`
                <div class="hub-exception-card" style="border-left: 4px solid ${n.border||"#10b981"};">
                    <div class="exception-card-header">
                        <span class="exception-title" style="color: #0f172a; font-weight: 600;">${n.title}</span>
                        <span class="${n.status_class||"delay-tag-ontime"}">${n.status}</span>
                    </div>
                    <div class="exception-card-body">${n.desc}</div>
                </div>
            `}),$("#tcd-audit-list").html(t)}},G=class{constructor(e){this.wrapper=e,this.currentCaseId=""}init(){this.bind_events(),this.load_copilot_context()}load_copilot_context(){let e=this;typeof frappe=="undefined"||!frappe.call||(frappe.call({method:"logistics_wizard.api.get_trade_case_list",callback:function(t){if(t&&Array.isArray(t.message)&&t.message.length>0){let n=$("#copilot-context-case");if(n.length){let i=t.message.map(s=>`<option value="${frappe.utils.escape_html(s.case_id)}">${frappe.utils.escape_html(s.case_id)}${s.party?" - "+frappe.utils.escape_html(s.party):""}</option>`).join("");n.html(i),e.currentCaseId&&t.message.some(s=>s.case_id===e.currentCaseId)||(e.currentCaseId=t.message[0].case_id),n.val(e.currentCaseId)}}}}),frappe.call({method:"logistics_wizard.api.get_rag_dashboard_metrics",args:{time_range:"7d",domain:"all"},callback:function(t){if(t&&t.message&&t.message.success&&t.message.data){let n=t.message.data,i=Number(n.active_chunks_count||n.live_chunks_count||0).toLocaleString("vi-VN"),a=Number(n.corpus_docs_count||n.committed_docs_count||0).toLocaleString("vi-VN");$("#copilot-rag-status-text").html(`<strong>RAG Corpus:</strong> ${i} Chunks (${a} v\u0103n b\u1EA3n)`)}}}))}on_tab_shown(e){e&&e.case_id&&(this.currentCaseId=e.case_id,$("#copilot-context-case").val(this.currentCaseId)),$("#copilot-input-textarea").focus()}bind_events(){let e=this;$(document).on("change","#copilot-context-case",function(){e.currentCaseId=$(this).val()}),$(document).on("click",".lw-starter-card",function(){let t=$(this).data("prompt")||$(this).find(".lw-card-title").text().trim();$("#copilot-input-textarea").val(t),e.send_message(t)}),$(document).on("click","#copilot-btn-send",function(){let t=$("#copilot-input-textarea").val().trim();t&&e.send_message(t)}),$(document).on("input","#copilot-input-textarea",function(){this.style.height="auto",this.style.height=Math.min(this.scrollHeight,160)+"px",$("#copilot-btn-send").prop("disabled",$(this).val().trim().length===0)}),$(document).on("keydown","#copilot-input-textarea",function(t){if(t.key==="Enter"&&!t.shiftKey){t.preventDefault();let n=$(this).val().trim();n&&e.send_message(n)}}),$(document).on("click","#copilot-btn-new-chat",function(){$("#copilot-chat-history").empty(),$(".lw-copilot-welcome-box").show(),$("#copilot-input-textarea").val("").css("height","auto").focus(),$("#copilot-btn-send").prop("disabled",!0),$(".lw-session-item").removeClass("active")}),$(document).on("click","#copilot-btn-clear",function(){$("#copilot-chat-history").empty(),$(".lw-copilot-welcome-box").show(),$("#copilot-input-textarea").val("").css("height","auto"),$("#copilot-btn-send").prop("disabled",!0)}),$(document).on("click",".lw-session-item",function(){$(".lw-session-item").removeClass("active"),$(this).addClass("active");let t=$(this).data("prompt")||$(this).find(".lw-session-title").text().trim();e.load_session_sample(t)}),$(document).on("input","#copilot-session-search",function(){let t=$(this).val().toLowerCase().trim();$(".lw-session-item").each(function(){let n=$(this).find(".lw-session-title").text().toLowerCase();$(this).toggle(n.includes(t))})}),$(document).on("click",".lw-thinking-header",function(){$(this).next(".lw-thinking-content").slideToggle(180),$(this).find(".fa-chevron-down, .fa-chevron-up").toggleClass("fa-chevron-down fa-chevron-up")}),$(document).on("click",".btn-copilot-copy",function(){let t=$(this).closest(".lw-chat-bubble").find(".lw-chat-text").text();navigator.clipboard&&(navigator.clipboard.writeText(t),frappe.show_alert({message:__("\u0110\xE3 sao ch\xE9p c\xE2u tr\u1EA3 l\u1EDDi v\xE0o clipboard!"),indicator:"green"}))}),$(document).on("click",".btn-copilot-view-cost",function(){typeof frappe!="undefined"&&frappe.set_route?frappe.set_route("trade-cost-dashboard"):e.wrapper&&e.wrapper.unifiedHub&&e.wrapper.unifiedHub.switch_tab("cost",{case_id:e.currentCaseId})}),$(document).on("click",".btn-copilot-view-tracking",function(){typeof frappe!="undefined"&&frappe.set_route?frappe.set_route("shipment-tracking-hub"):e.wrapper&&e.wrapper.unifiedHub&&e.wrapper.unifiedHub.switch_tab("tracking")})}send_message(e){$(".lw-copilot-welcome-box").hide(),$("#copilot-input-textarea").val("").css("height","auto"),$("#copilot-btn-send").prop("disabled",!0);let t=`
            <div class="lw-chat-message lw-chat-user">
                <div class="lw-chat-avatar"><i class="fa fa-user"></i></div>
                <div class="lw-chat-bubble">
                    <div class="lw-chat-text">${frappe.utils.escape_html(e)}</div>
                </div>
            </div>
        `;$("#copilot-chat-history").append(t),this.scroll_to_bottom();let n=this,i="ai-msg-"+Date.now(),a=`
            <div class="lw-chat-message lw-chat-assistant" id="${i}">
                <div class="lw-chat-avatar">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                    </svg>
                </div>
                <div class="lw-chat-bubble">
                    <div class="lw-thinking-block">
                        <div class="lw-thinking-header">
                            <i class="fa fa-circle-o-notch fa-spin" style="color: #0284c7;"></i>
                            <span>AI \u0111ang suy lu\u1EADn & truy xu\u1EA5t kho tri th\u1EE9c...</span>
                        </div>
                    </div>
                    <div class="lw-chat-text" style="color: #64748b; font-size: 13px;">
                        <i class="fa fa-circle-o-notch fa-spin"></i> \u0110ang chu\u1EA9n b\u1ECB ph\u1EA3n h\u1ED3i chuy\xEAn s\xE2u...
                    </div>
                </div>
            </div>
        `;$("#copilot-chat-history").append(a),n.scroll_to_bottom(),typeof frappe!="undefined"&&frappe.call?frappe.call({method:"logistics_wizard.api.ask_ai_copilot",args:{query:e,case_id:n.currentCaseId||$("#copilot-context-case").val()||void 0},callback:function(s){if(s&&s.message&&s.message.success)s.message.case_id&&(n.currentCaseId=s.message.case_id,$("#copilot-context-case").val(s.message.case_id)),n.render_assistant_response(i,s.message);else{let l=s&&s.message&&s.message.error||"L\u1ED7i x\u1EED l\xFD c\xE2u h\u1ECFi t\u1EEB h\u1EC7 th\u1ED1ng";$(`#${i} .lw-chat-bubble`).html(`<span style="color:#ef4444;"><i class="fa fa-exclamation-triangle"></i> L\u1ED7i: ${frappe.utils.escape_html(l)}</span>`)}n.scroll_to_bottom()},error:function(s){$(`#${i} .lw-chat-bubble`).html('<span style="color:#ef4444;"><i class="fa fa-exclamation-triangle"></i> L\u1ED7i k\u1EBFt n\u1ED1i API</span>'),n.scroll_to_bottom()}}):setTimeout(()=>{n.generate_fallback_response(i,e)},500)}render_assistant_response(e,t){let n="";t.thinking&&(n=`
                <div class="lw-thinking-block">
                    <div class="lw-thinking-header">
                        <i class="fa fa-lightbulb-o" style="color: #0284c7;"></i>
                        <span>Qu\xE1 tr\xECnh suy lu\u1EADn & truy xu\u1EA5t d\u1EEF li\u1EC7u (Ho\xE0n t\u1EA5t)</span>
                        <i class="fa fa-chevron-down" style="margin-left: auto; font-size: 10px;"></i>
                    </div>
                    <div class="lw-thinking-content" style="display: none;">
                        <pre style="margin: 0; background: transparent; border: none; font-size: 11.5px; color: #475569; padding: 0; white-space: pre-wrap; font-family: monospace;">${frappe.utils.escape_html(t.thinking)}</pre>
                    </div>
                </div>
            `);let i="";Array.isArray(t.sources)&&t.sources.length&&(i=`
                <div class="lw-chat-sources">
                    <span class="lw-sources-label"><i class="fa fa-bookmark-o"></i> Ngu\u1ED3n tham chi\u1EBFu:</span>
                    ${t.sources.map(l=>`<span class="lw-source-pill" title="${frappe.utils.escape_html(l.snippet||"")}"><i class="fa fa-file-text-o"></i> ${frappe.utils.escape_html(l.title)}</span>`).join("")}
                </div>
            `);let a=`
            <div class="lw-chat-actions">
                <button class="lw-chat-action-btn btn-copilot-copy"><i class="fa fa-copy"></i> Sao ch\xE9p</button>
                <button class="lw-chat-action-btn btn-copilot-view-cost"><i class="fa fa-calculator"></i> B\u1EA3ng chi ph\xED</button>
                <button class="lw-chat-action-btn btn-copilot-view-tracking"><i class="fa fa-ship"></i> Tra c\u1EE9u h\xE0nh tr\xECnh</button>
            </div>
        `,s=`
            ${n}
            <div class="lw-chat-text">${t.answer||""}</div>
            ${i}
            ${a}
        `;$(`#${e} .lw-chat-bubble`).html(s),this.scroll_to_bottom()}generate_fallback_response(e,t){let i=`
            <div class="lw-chat-text">
                <p>H\u1EC7 th\u1ED1ng Logistics Wizard \u0111\xE3 k\u1EBFt n\u1ED1i v\u1EDBi h\u1ED3 s\u01A1 <strong>${this.currentCaseId||"IMP-2026-001"}</strong> v\xE0 c\u01A1 s\u1EDF tri th\u1EE9c RAG.</p>
            </div>
        `;$(`#${e} .lw-chat-bubble`).html(i),this.scroll_to_bottom()}scroll_to_bottom(){let e=$("#copilot-messages-thread");e.length&&e.stop().animate({scrollTop:e[0].scrollHeight},150)}load_session_sample(e){$("#copilot-chat-history").empty(),$(".lw-copilot-welcome-box").hide(),this.send_message(e)}};typeof window!="undefined"&&(window.ShipmentTrackingHub=F,window.TradeCaseOverviewController=V,window.UnifiedLogisticsHub=B,window.EmbeddedTradeCostDashboardController=K,window.EmbeddedLogisticsAICopilot=G,window.init_logistics_hub_page=Q,window.show_logistics_hub_page=U,window.register_logistics_hub_page=te);typeof global!="undefined"&&(global.ShipmentTrackingHub=F,global.TradeCaseOverviewController=V,global.UnifiedLogisticsHub=B,global.EmbeddedTradeCostDashboardController=K,global.EmbeddedLogisticsAICopilot=G,global.init_logistics_hub_page=Q,global.show_logistics_hub_page=U,global.register_logistics_hub_page=te);(function(){"use strict";if(typeof window=="undefined")return;function p(){if($("#logistics-ai-fab-container").length||typeof frappe!="undefined"&&frappe.session&&frappe.session.user==="Guest")return;let t=`
            <!-- FLOATING ACTION BUTTON (FAB) -->
            <div id="logistics-ai-fab-container">
                <span class="fab-tooltip-pill">Tr\u1EE3 l\xFD Logistics AI</span>
                <button id="btn-logistics-fab" class="logistics-fab-btn" title="M\u1EDF Tr\u1EE3 l\xFD AI Logistics">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                    <span class="fab-badge-dot"></span>
                </button>
            </div>

            <!-- POPUP CHAT DRAWER -->
            <div id="logistics-ai-drawer" style="display: none;">
                <div class="drawer-header">
                    <div class="drawer-header-brand">
                        <div class="drawer-avatar">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                            </svg>
                        </div>
                        <div class="drawer-header-info">
                            <span class="drawer-title">Logistics Copilot</span>
                            <span class="drawer-sub">\u25CF Tr\u1EF1c tuy\u1EBFn & S\u1EB5n s\xE0ng</span>
                        </div>
                    </div>
                    <div class="drawer-header-actions">
                        <button id="btn-drawer-rag-admin" class="drawer-action-btn" title="Kho tri th\u1EE9c RAG">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                                <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
                                <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                            </svg>
                        </button>
                        <button id="btn-drawer-fullscreen" class="drawer-action-btn" title="M\u1EDF trang \u0111\u1EA7y \u0111\u1EE7">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="15 3 21 3 21 9"></polyline>
                                <polyline points="9 21 3 21 3 15"></polyline>
                                <line x1="21" y1="3" x2="14" y2="10"></line>
                                <line x1="3" y1="21" x2="10" y2="14"></line>
                            </svg>
                        </button>
                        <button id="btn-drawer-close" class="drawer-action-btn" title="Thu nh\u1ECF v\u1EC1 ch\u1EA5m tr\xF2n">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                </div>

                <div id="drawer-messages-body" class="drawer-body">
                    <div id="drawer-welcome-state" class="drawer-welcome-box">
                        <div class="drawer-welcome-icon">\u{1F6A2}</div>
                        <div class="drawer-welcome-text">
                            <strong>Xin ch\xE0o!</strong> T\xF4i l\xE0 Tr\u1EE3 l\xFD AI chuy\xEAn tr\xE1ch v\u1EC1 Bi\u1EC3u thu\u1EBF XNK, Th\xF4ng t\u01B0 85, Landed Cost v\xE0 h\xE0nh tr\xECnh t\xE0u.
                        </div>
                        <div class="drawer-quick-prompts">
                            <button class="drawer-prompt-btn" data-q="Theo Th\xF4ng t\u01B0 85/2026/TT-BTC, m\xE1y m\xF3c thi\u1EBFt b\u1ECB th\xE1o r\u1EDDi \u0111\u01B0\u1EE3c ph\xE2n lo\u1EA1i theo quy t\u1EAFc n\xE0o?">
                                \u{1F4DC} Th\xF4ng t\u01B0 85 & M\xE1y m\xF3c th\xE1o r\u1EDDi
                            </button>
                            <button class="drawer-prompt-btn" data-q="Ph\xE2n t\xEDch chi ti\u1EBFt sai l\u1EC7ch chi ph\xED th\u1EF1c t\u1EBF so v\u1EDBi d\u1EF1 to\xE1n cho h\u1ED3 s\u01A1 \u0111ang m\u1EDF">
                                \u{1F4CA} Ph\xE2n t\xEDch sai l\u1EC7ch chi ph\xED h\u1ED3 s\u01A1
                            </button>
                            <button class="drawer-prompt-btn" data-q="Ki\u1EC3m tra tr\u1EA1ng th\xE1i v\u1EADn chuy\u1EC3n, tuy\u1EBFn c\u1EA3ng v\xE0 ETA m\u1EDBi nh\u1EA5t c\u1EE7a h\u1ED3 s\u01A1 \u0111ang m\u1EDF">
                                \u{1F6A2} Theo d\xF5i h\xE0nh tr\xECnh & ETA
                            </button>
                            <button class="drawer-prompt-btn btn-open-rag-admin-center" style="border-left: 3px solid #0284c7; background: #f0f9ff; font-weight: 600; color: #0369a1; text-align: left;">
                                \u2699\uFE0F Qu\u1EA3n tr\u1ECB RAG & Kho Tri Th\u1EE9c HS &rarr;
                            </button>
                        </div>
                    </div>
                </div>

                <div class="drawer-footer">
                    <div class="drawer-input-row">
                        <textarea id="drawer-textarea" class="drawer-textarea" placeholder="H\u1ECFi nhanh AI Logistics... (Enter g\u1EEDi)" rows="1"></textarea>
                        <button id="btn-drawer-send" class="drawer-btn-send" disabled title="G\u1EEDi c\xE2u h\u1ECFi">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                                <line x1="12" y1="19" x2="12" y2="5"></line>
                                <polyline points="5 12 12 5 19 12"></polyline>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;$("body").append(t),e()}function e(){let t=$("#btn-logistics-fab"),n=$("#logistics-ai-drawer"),i=$("#drawer-textarea"),a=$("#btn-drawer-send"),s=$("#drawer-messages-body"),l=$("#drawer-welcome-state");t.on("click",function(r){r.stopPropagation(),n.is(":visible")?n.fadeOut(150):(n.fadeIn(180),i.focus())}),$("#btn-drawer-close").on("click",function(){n.fadeOut(150)}),$(document).on("click","#btn-drawer-rag-admin, .btn-open-rag-admin-center",function(r){r.preventDefault(),n.fadeOut(150),typeof frappe!="undefined"&&frappe.set_route?frappe.set_route("rag-knowledge-base"):window.location.href="/app/rag-knowledge-base"}),$("#btn-drawer-fullscreen").on("click",function(){n.fadeOut(150),typeof frappe!="undefined"&&frappe.set_route?frappe.set_route("logistics-ai-copilot"):window.location.href="/app/logistics-ai-copilot"}),i.on("input",function(){this.style.height="auto",this.style.height=Math.min(this.scrollHeight,120)+"px",a.prop("disabled",$(this).val().trim().length===0)}),i.on("keydown",function(r){r.key==="Enter"&&!r.shiftKey&&(r.preventDefault(),c())}),a.on("click",function(){c()}),$(".drawer-prompt-btn").on("click",function(){let r=$(this).data("q");r&&(i.val(r),i.trigger("input"),c())});function c(){let r=i.val().trim();if(!r)return;l.hide(),i.val("").css("height","auto"),a.prop("disabled",!0),d("user",r);let h=d("assistant",'<span class="typing-dots"><i class="fa fa-circle-o-notch fa-spin"></i> \u0110ang suy lu\u1EADn...</span>'),v=$("#tc-case-selector").val()||$("#tcd-case-selector").val()||$("#copilot-context-case").val()||void 0;typeof frappe!="undefined"&&frappe.call?frappe.call({method:"logistics_wizard.api.ask_ai_copilot",args:{query:r,case_id:v,drawer:!0},callback:function(f){if(f&&f.message&&f.message.success){let y=f.message,C="";if(y.thinking){let S=y.thinking.split(`
`)[0]||"Truy xu\u1EA5t RAG";C+=`<div class="drawer-thinking-mini">\u{1F4A1} <em>${frappe.utils.escape_html(S)}</em></div>`}C+=`<div class="drawer-answer-content">${y.answer||""}</div>`,Array.isArray(y.sources)&&y.sources.length&&(C+=`<div class="drawer-sources-mini"><strong>Ngu\u1ED3n:</strong> ${y.sources.map(S=>frappe.utils.escape_html(S.title)).join(", ")}</div>`),h.find(".drawer-msg-bubble").html(C)}else{let y=f&&f.message&&f.message.error||"L\u1ED7i x\u1EED l\xFD c\xE2u h\u1ECFi";h.find(".drawer-msg-bubble").html(`<span style="color:#ef4444;"><i class="fa fa-exclamation-triangle"></i> L\u1ED7i: ${frappe.utils.escape_html(y)}</span>`)}o()},error:function(){h.find(".drawer-msg-bubble").html('<span style="color:#ef4444;"><i class="fa fa-exclamation-triangle"></i> L\u1ED7i k\u1EBFt n\u1ED1i API</span>'),o()}}):setTimeout(()=>{h.find(".drawer-msg-bubble").html("H\u1EC7 th\u1ED1ng AI Copilot \u0111ang tr\u1EF1c tuy\u1EBFn."),o()},400)}function d(r,h){let f=r==="user"?frappe.utils.escape_html(h).replace(/\n/g,"<br>"):h,y=$(`
                <div class="drawer-msg-row ${r}">
                    <div class="drawer-msg-bubble">
                        ${f}
                    </div>
                </div>
            `);return s.append(y),o(),y}function o(){s.stop().animate({scrollTop:s[0].scrollHeight},100)}if(typeof frappe!="undefined"){let r=frappe.get_route&&frappe.get_route()||[];Array.isArray(r)&&(r[1]==="logistics-ai-copilot"||r[1]==="logistics_ai_copilot")&&($("#logistics-ai-fab-container").hide(),$("#logistics-ai-drawer").hide()),frappe.router&&frappe.router.on&&frappe.router.on("change",function(){let h=frappe.get_route&&frappe.get_route()||[];Array.isArray(h)&&(h[1]==="logistics-ai-copilot"||h[1]==="logistics_ai_copilot")?($("#logistics-ai-fab-container").hide(),$("#logistics-ai-drawer").hide()):$("#logistics-ai-fab-container").show()})}}typeof frappe!="undefined"&&frappe.ready?frappe.ready(p):$(document).ready(p),typeof window!="undefined"&&(window.initLogisticsAIWidget=p)})();})();
//# sourceMappingURL=unified_logistics_hub.bundle.U7GC2DF7.js.map
