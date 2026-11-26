// Copyright (c) 2026, Logistics Wizard and contributors
// For license information, please see license.txt

/**
 * Customs Declaration Form Controller — Module 4 (Customs & Trade Compliance)
 * Integrates AI/RAG HS Recommendation + Strict Human Specialist Approval Gate.
 */

function _lw_build_item_options(frm) {
	const items = frm.doc.items || [];
	return items.map((row, idx) => {
		const n = idx + 1;
		const title = row.item_name || row.item_code || `Dòng hàng #${n}`;
		const hs = row.approved_hs_code || row.suggested_hs_code || 'Chưa có HS';
		const st = row.hs_approval_status || 'Pending';
		return `${n} | ${title} [${hs} - ${st}]`;
	});
}

function _lw_parse_item_idx(selectedLabel) {
	const m = String(selectedLabel || '1').match(/^(\d+)/);
	return m ? parseInt(m[1], 10) : 1;
}

function _lw_render_rag_candidates_html(res, declarationName, itemIdx) {
	const esc = frappe.utils.escape_html;
	const candidates = res.candidates || [];
	const notes = res.legal_notes || [];
	const engine = res.retrieval_engine || 'postgres_rag_graph';

	const rowsHtml = candidates.map((c, i) => {
		const isTop = i === 0;
		const badgeBg = c.confidence_score >= 75 ? '#0f766e' : (c.confidence_score >= 55 ? '#0369a1' : '#d97706');
		return `
			<tr style="${isTop ? 'background:#f0fdfa;' : ''}">
				<td style="white-space:nowrap; font-weight:700; color:#0f172a;">
					${esc(c.hs_code)}
					${isTop ? '<div style="font-size:10px; color:#0f766e; font-weight:600;">ĐỀ XUẤT #1</div>' : ''}
				</td>
				<td>
					<div style="font-weight:600; color:#1e293b;">${esc(c.description || '')}</div>
					<div style="font-size:11px; color:#475569; margin-top:2px;">${esc(c.full_hierarchy_path || '')}</div>
				</td>
				<td style="text-align:center; white-space:nowrap;">
					<span style="display:inline-block; padding:2px 8px; border-radius:999px; background:${badgeBg}; color:#fff; font-weight:600; font-size:11px;">
						${flt(c.confidence_score, 1)}%
					</span>
				</td>
				<td style="text-align:right; white-space:nowrap;">
					<button type="button" class="btn btn-xs btn-default lw-pick-hs-candidate"
						data-hs="${esc(c.hs_code)}"
						data-conf="${flt(c.confidence_score, 1)}"
						data-basis="${esc(c.legal_basis || '')}"
						data-decl="${esc(declarationName || '')}"
						data-idx="${itemIdx}">
						Chọn đề xuất
					</button>
				</td>
			</tr>
		`;
	}).join('');

	const notesHtml = notes.length
		? notes.slice(0, 4).map(n =>
			`<li style="margin-bottom:4px;"><b>${esc(n.id || n.chunk_type || 'Chú giải')}</b>: ${esc(n.text || '')}</li>`
		).join('')
		: '<li>Áp dụng Quy tắc tổng quát GIR 1 &amp; GIR 6 theo Thông tư 31/2022/TT-BTC.</li>';

	const llmBox = res.llm_reasoning && res.llm_reasoning.gir_rationale_vi
		? `<div style="margin-top:10px; padding:10px 12px; background:#eff6ff; border-left:3px solid #0369a1; border-radius:4px; font-size:12px;">
			<b>Phân tích chuyên sâu (LLM / ${esc(res.llm_reasoning.model || 'CLIProxyAPI')}):</b><br>
			${esc(res.llm_reasoning.gir_rationale_vi)}
		</div>`
		: '';

	return `
		<div style="font-size:12px; color:#334155;">
			<div style="padding:8px 12px; background:#fef3c7; border:1px solid #f59e0b; border-radius:6px; margin-bottom:10px; color:#92400e;">
				<b>Nguyên tắc Quản trị HS (Human-in-the-Loop):</b> AI/RAG chỉ ghi nhận trạng thái <b>Proposed (Đề xuất)</b> kèm căn cứ pháp lý.
				Mã HS <b>chưa được phê duyệt tự động</b> cho tới khi Chuyên viên Hải quan thẩm định và bấm <b>Phê duyệt HS</b>.
			</div>
			<div style="margin-bottom:8px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:6px;">
				<span><b>Truy vấn:</b> ${esc(res.query || '')}</span>
				<span style="color:#0f766e;"><b>Nguồn truy xuất:</b> ${esc(engine)}</span>
			</div>
			<table class="table table-bordered table-condensed" style="font-size:12px; margin-bottom:10px;">
				<thead>
					<tr style="background:#f8fafc;">
						<th>Mã HS (8 số)</th>
						<th>Mô tả &amp; Phân cấp Biểu thuế TT31</th>
						<th style="text-align:center;">Độ tin cậy</th>
						<th style="text-align:right;">Thao tác</th>
					</tr>
				</thead>
				<tbody>${rowsHtml}</tbody>
			</table>
			${llmBox}
			<div style="margin-top:10px; padding:8px 12px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px;">
				<div style="font-weight:700; color:#0f172a; margin-bottom:4px;">Căn cứ Pháp lý &amp; Chú giải Biểu thuế</div>
				<ul style="padding-left:18px; margin-bottom:0; font-size:11.5px;">${notesHtml}</ul>
			</div>
		</div>
	`;
}

function _lw_open_hs_approval_dialog(frm, defaultIdx) {
	const itemOptions = _lw_build_item_options(frm);
	if (!itemOptions.length) {
		frappe.msgprint(__('Tờ khai chưa có dòng hàng nào để phê duyệt mã HS.'));
		return;
	}
	const idx0 = Math.max(0, Math.min((defaultIdx || 1) - 1, frm.doc.items.length - 1));
	const row0 = frm.doc.items[idx0];

	const d = new frappe.ui.Dialog({
		title: __('Phê duyệt / Từ chối Mã HS (Chuyên viên Hải quan)'),
		fields: [
			{
				fieldname: 'item_selector',
				fieldtype: 'Select',
				label: __('Chọn dòng hàng cần thẩm định'),
				options: itemOptions.join('\n'),
				default: itemOptions[idx0],
				reqd: 1,
				onchange: function() {
					const idx = _lw_parse_item_idx(d.get_value('item_selector'));
					const r = (frm.doc.items || [])[idx - 1];
					if (r) {
						d.set_value('suggested_hs_preview', r.suggested_hs_code || '');
						d.set_value('legal_basis_preview', r.hs_legal_basis || '');
						d.set_value('approved_hs_code', r.approved_hs_code || r.suggested_hs_code || '');
					}
				}
			},
			{
				fieldname: 'suggested_hs_preview',
				fieldtype: 'Data',
				label: __('Mã HS đang được đề xuất'),
				default: row0.suggested_hs_code || '',
				read_only: 1
			},
			{
				fieldname: 'legal_basis_preview',
				fieldtype: 'Small Text',
				label: __('Căn cứ pháp lý / Evidence từ AI/RAG'),
				default: row0.hs_legal_basis || '',
				read_only: 1
			},
			{
				fieldname: 'action',
				fieldtype: 'Select',
				label: __('Quyết định thẩm định'),
				options: 'approve\nreject',
				default: 'approve',
				reqd: 1
			},
			{
				fieldname: 'approved_hs_code',
				fieldtype: 'Data',
				label: __('Mã HS chính thức (Chuyên viên xác nhận / điều chỉnh)'),
				default: row0.approved_hs_code || row0.suggested_hs_code || ''
			},
			{
				fieldname: 'notes',
				fieldtype: 'Small Text',
				label: __('Ghi chú thẩm định chuyên viên'),
				default: row0.approval_notes || ''
			}
		],
		primary_action_label: __('Xác nhận quyết định HS'),
		primary_action: function(vals) {
			const idx = _lw_parse_item_idx(vals.item_selector);
			frappe.call({
				method: 'logistics_wizard.customs_engine.api.approve_hs_code',
				args: {
					declaration_name: frm.doc.name,
					item_idx: idx,
					action: vals.action,
					approved_hs_code: vals.approved_hs_code || undefined,
					notes: vals.notes || undefined
				},
				freeze: true,
				freeze_message: __('Đang ghi nhận quyết định phê duyệt HS...'),
				callback: function(r) {
					const res = (r && r.message) || {};
					if (res.success) {
						d.hide();
						frappe.show_alert({
							message: vals.action === 'approve'
								? __(`Chuyên viên đã phê duyệt mã HS ${res.approved_hs_code} (dòng #${idx})`)
								: __(`Đã từ chối đề xuất HS dòng #${idx}`),
							indicator: vals.action === 'approve' ? 'green' : 'orange'
						});
						frm.reload_doc();
					} else {
						frappe.msgprint({
							title: __('Không thể phê duyệt mã HS'),
							indicator: 'red',
							message: res.error || __('Vui lòng kiểm tra mã HS hợp lệ (4-10 chữ số).')
						});
					}
				}
			});
		}
	});
	d.show();
}

frappe.ui.form.on('Customs Declaration', {
	refresh: function(frm) {
		frm.trigger('render_hs_governance_banner');

		if (frm.is_new()) {
			return;
		}

		// 1. AI/RAG HS Suggestion Button (Never auto-approves)
		frm.add_custom_button(__('Gợi ý mã HS (AI/RAG)'), function() {
			const itemOptions = _lw_build_item_options(frm);
			if (!itemOptions.length) {
				frappe.msgprint(__('Vui lòng thêm ít nhất 1 dòng hàng trong bảng hàng hóa trước khi chạy AI/RAG gợi ý mã HS.'));
				return;
			}
			const row0 = frm.doc.items[0];
			const defaultDesc = [row0.item_name, row0.description].filter(Boolean).join(' - ');

			const promptDlg = new frappe.ui.Dialog({
				title: __('AI/RAG Tra cứu & Đề xuất Mã HS (TT31/AHTN)'),
				fields: [
					{
						fieldname: 'item_selector',
						fieldtype: 'Select',
						label: __('Dòng hàng cần phân loại'),
						options: itemOptions.join('\n'),
						default: itemOptions[0],
						reqd: 1,
						onchange: function() {
							const idx = _lw_parse_item_idx(promptDlg.get_value('item_selector'));
							const r = (frm.doc.items || [])[idx - 1];
							if (r) {
								promptDlg.set_value(
									'item_description',
									[r.item_name, r.description].filter(Boolean).join(' - ')
								);
							}
						}
					},
					{
						fieldname: 'item_description',
						fieldtype: 'Small Text',
						label: __('Tên & Mô tả kỹ thuật hàng hóa'),
						default: defaultDesc,
						reqd: 1
					},
					{
						fieldname: 'material',
						fieldtype: 'Data',
						label: __('Chất liệu cấu thành (Tùy chọn)')
					},
					{
						fieldname: 'function',
						fieldtype: 'Data',
						label: __('Công dụng / Nguyên lý hoạt động (Tùy chọn)')
					},
					{
						fieldname: 'use_llm',
						fieldtype: 'Check',
						label: __('Kích hoạt phân tích sâu GIR bằng LLM (CLIProxyAPI)'),
						default: 0
					}
				],
				primary_action_label: __('Tra cứu & Đề xuất HS'),
				primary_action: function(vals) {
					const idx = _lw_parse_item_idx(vals.item_selector);
					frappe.call({
						method: 'logistics_wizard.customs_engine.api.suggest_hs_code_with_rag',
						args: {
							declaration_name: frm.doc.name,
							item_idx: idx,
							item_description: vals.item_description,
							material: vals.material || undefined,
							function: vals.function || undefined,
							auto_propose: true,
							use_llm: Boolean(vals.use_llm)
						},
						freeze: true,
						freeze_message: __('Đang truy xuất Biểu thuế & Đồ thị tri thức Pháp lý Hải quan (AI/RAG)...'),
						callback: function(r) {
							const res = (r && r.message) || {};
							if (!res.success) {
								frappe.msgprint({
									title: __('Không tìm thấy mã HS phù hợp'),
									indicator: 'orange',
									message: res.error || __('Vui lòng bổ sung mô tả chi tiết hơn.')
								});
								return;
							}
							promptDlg.hide();
							const resDlg = new frappe.ui.Dialog({
								title: __(`Kết quả AI/RAG HS — Dòng #${idx} (Trạng thái: Proposed)`),
								size: 'large',
								fields: [
									{
										fieldname: 'results_html',
										fieldtype: 'HTML',
										options: _lw_render_rag_candidates_html(res, frm.doc.name, idx)
									}
								],
								primary_action_label: __('Chuyển sang Phê duyệt Chuyên viên'),
								primary_action: function() {
									resDlg.hide();
									frm.reload_doc().then(() => _lw_open_hs_approval_dialog(frm, idx));
								}
							});
							resDlg.show();

							// Bind candidate override selection button
							resDlg.$wrapper.on('click', '.lw-pick-hs-candidate', function() {
								const $btn = $(this);
								frappe.call({
									method: 'logistics_wizard.customs_engine.api.propose_hs_code',
									args: {
										declaration_name: frm.doc.name,
										item_idx: idx,
										suggested_hs_code: $btn.data('hs'),
										confidence_score: $btn.data('conf'),
										legal_basis: $btn.data('basis'),
										source: 'AI/RAG Suggestion'
									},
									callback: function(pr) {
										if (pr && pr.message && pr.message.success) {
											frappe.show_alert({
												message: __(`Đã chọn mã ${pr.message.suggested_hs_code} làm Đề xuất (Proposed) cho dòng #${idx}`),
												indicator: 'blue'
											});
											frm.reload_doc();
										}
									}
								});
							});

							frm.reload_doc();
						}
					});
				}
			});
			promptDlg.show();
		}, __('AI & Tuân thủ HS'));

		// 2. Specialist Human Approval Gate Button
		frm.add_custom_button(__('Phê duyệt / Từ chối HS (Chuyên viên)'), function() {
			_lw_open_hs_approval_dialog(frm, 1);
		}, __('AI & Tuân thủ HS'));

		// 3. Advance Workflow Button
		frm.add_custom_button(__('Chuyển bước Quy trình Hải quan'), function() {
			frappe.prompt([
				{
					fieldname: 'target_status',
					fieldtype: 'Select',
					label: __('Trạng thái đích'),
					options: 'Ready\nDeclared\nProcessing\nCleared\nRejected\nPreparing',
					default: frm.doc.workflow_status === 'Preparing' ? 'Ready' : 'Declared',
					reqd: 1
				},
				{
					fieldname: 'declaration_no',
					fieldtype: 'Data',
					label: __('Số tờ khai VNACCS/VCIS'),
					default: frm.doc.declaration_no || ''
				},
				{
					fieldname: 'customs_lane',
					fieldtype: 'Select',
					label: __('Phân luồng Hải quan'),
					options: 'Not Declared\nGreen\nYellow\nRed',
					default: frm.doc.customs_lane || 'Green'
				},
				{
					fieldname: 'rejection_reason',
					fieldtype: 'Small Text',
					label: __('Lý do từ chối (nếu Rejected)')
				}
			], function(vals) {
				frappe.call({
					method: 'logistics_wizard.customs_engine.api.advance_customs_workflow',
					args: {
						declaration_name: frm.doc.name,
						target_status: vals.target_status,
						declaration_no: vals.declaration_no || undefined,
						customs_lane: vals.customs_lane,
						rejection_reason: vals.rejection_reason || undefined
					},
					callback: function(r) {
						const res = (r && r.message) || {};
						if (res.success) {
							frappe.show_alert({
								message: __(`Đã chuyển tờ khai sang ${res.workflow_status} (Luồng: ${res.customs_lane})`),
								indicator: 'green'
							});
							frm.reload_doc();
						} else {
							frappe.msgprint({
								title: __('Chặn chuyển trạng thái Hải quan'),
								indicator: 'red',
								message: res.error || __('Không thể chuyển trạng thái.')
							});
						}
					}
				});
			}, __('Chuyển bước Quy trình Tờ khai'), __('Xác nhận'));
		}, __('Hải quan'));
	},

	render_hs_governance_banner: function(frm) {
		frm.dashboard.clear_headline();
		const items = frm.doc.items || [];
		if (!items.length) {
			return;
		}
		const pendingCount = items.filter(it => it.hs_approval_status !== 'Approved').length;
		if (pendingCount > 0) {
			frm.dashboard.set_headline(
				`<span style="color:#b45309; font-weight:600;">
					Còn ${pendingCount}/${items.length} dòng hàng chưa được Chuyên viên Hải quan phê duyệt mã HS (chặn truyền tờ khai Declared).
				</span>`
			);
		} else {
			frm.dashboard.set_headline(
				`<span style="color:#0f766e; font-weight:600;">
					Toàn bộ ${items.length}/${items.length} dòng hàng đã được Chuyên viên phê duyệt mã HS hợp lệ.
				</span>`
			);
		}
	}
});
