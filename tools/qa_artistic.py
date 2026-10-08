"""Opt-in dual verification in the existing QA receipt. Declared reviews, not AI vision.

Builds a blind objective critic packet, validates its returned delta and computes
bounded correction decisions. Never writes the asset, contract or capture files.
"""
import copy
import json
from pathlib import Path

import model_contract
import qa_freshness as fresh

GATES = {'SIMPLE':('FINAL',), 'STANDARD':('PRIMARY_FORMS','FINAL'),
         'COMPLEX':('PRIMARY_FORMS','CRITICAL_FEATURES','FINAL')}
VERDICTS = {'ACCEPTED','ACCEPTED_WITH_MINOR_DIFFERENCES','REVISION_REQUIRED','ESCALATE'}
VIEWS = ('front','side','back','three_quarter','high_45','low_45')
CRITICAL = {'CHARACTER':'face, hair, characteristic clothing', 'VEHICLE':'body, cabin, wheels, recognizable forms',
            'ENVIRONMENT':'architecture, composition, object scale', 'OTHER':'declared identity features'}


def require(ok, message):
    fresh.require(ok, message)


def exact(row, fields, label):
    fresh.exact(row, fields, label)


def strings(value, label, *, nonempty=False):
    require(isinstance(value, list) and (value or not nonempty)
            and all(isinstance(x, str) and x.strip() for x in value)
            and len(value) == len(set(value)), label + ': unique strings required')


def gates(complexity, *, local=False):
    require(complexity in GATES and type(local) is bool, 'invalid review complexity/scope')
    return ('LOCAL',) if local else GATES[complexity]


def critic_packet(brief, images, freshness, *, root, verify_artifact, accepted=()):
    """Allowlist objective inputs; no implementer verdict, rationale or chat history."""
    exact(brief, ('complexity','stage','asset_type','scope','requirements','contract','references',
                  'protected','constraints','implementer'), 'critic brief')
    require(brief['scope'] in ('FULL','LOCAL') and brief['stage'] in gates(brief['complexity'],local=brief['scope']=='LOCAL'),
            'review stage not selected by adaptive gates')
    require(brief['asset_type'] in CRITICAL and isinstance(brief['implementer'], str) and brief['implementer'].strip(),
            'asset type/implementer required')
    strings(brief['protected'], 'protected regions')
    strings(brief['constraints'], 'user constraints')
    if brief['scope'] == 'FULL':
        require(set(brief['protected']) <= set(brief['requirements']), 'protected regions need full review coverage')
        coverage = {v for r in brief['requirements'].values() for v in r['views']}
        needed = set(VIEWS if brief['stage'] == 'FINAL' else ('front','side','three_quarter'))
        require(needed <= coverage, 'standard stage views cannot be cherry-picked')
    exact(brief['contract'], ('artifact','ref'), 'critic Model Contract binding')
    exact(brief['contract']['ref'], ('id','revision','sha256'), 'Model Contract ref')
    verify_artifact(brief['contract']['artifact'], 'PASS0', root, png_only=False)
    require(root is not None, 'critic packet requires file verification')
    pass0 = json.loads((Path(root)/brief['contract']['artifact']['path']).read_text(encoding='utf-8-sig'))
    require(not model_contract.validate_contract(pass0), 'critic requires a valid locked Model Contract')
    require(model_contract.reference(pass0) == brief['contract']['ref'], 'critic cannot revise Model Contract/Identity Lock')
    require(isinstance(brief['references'], dict) and brief['references'], 'canonical references required')
    authoritative = {s['id']:s for s in pass0['sources'] if s['id'] in pass0['source_of_truth']}
    require(set(brief['references']) == set(authoritative), 'critic needs all canonical references; no auxiliary substitution')
    for key, image in brief['references'].items():
        verify_artifact(image, 'canonical reference '+key, root)
        fresh.png_integrity(Path(root)/image['path'])
        require(image == {k:authoritative[key][k] for k in ('path','sha256')}, 'canonical reference changed')
    sufficiency = fresh.sufficient(brief['requirements'], images, freshness)
    # All objectively suitable views, not just the implementer's chosen favorite.
    captures = []
    for cid, image in sorted(images.items()):
        status = freshness.get(cid, {})
        if image['phase'] == 'AFTER' and any(status.get('regions', {}).get(r) == 'CURRENT' for r in brief['requirements']):
            captures.append({k:copy.deepcopy(image[k]) for k in ('id','image','setup','phase')}
                            | {'view':image.get('view','closeup'), 'freshness':copy.deepcopy(status)})
    return dict(mode='ARTISTIC_REVIEW', stage=brief['stage'], asset_type=brief['asset_type'],
                complexity=brief['complexity'], scope=brief['scope'],
                criteria=CRITICAL[brief['asset_type']] if brief['stage']=='CRITICAL_FEATURES' else
                    'reference silhouette, proportions and primary volumes' if brief['stage']=='PRIMARY_FORMS' else 'scoped final reference likeness',
                contract_ref=copy.deepcopy(brief['contract']['ref']),
                model_contract=copy.deepcopy(pass0['model_contract']), design=model_contract.identity(pass0),
                references=copy.deepcopy(brief['references']), protected=copy.deepcopy(brief['protected']),
                accepted=sorted(accepted),
                constraints=copy.deepcopy(brief['constraints']), requirements=copy.deepcopy(brief['requirements']),
                captures=captures, sufficiency=sufficiency)


def checkpoint_from_receipt(previous, artifact, *, root, verify_artifact, _depth=0):
    """Compact memory derived from the preceding existing QA receipt, not a new log."""
    require(isinstance(previous,dict) and previous.get('schema_version') in (1,2,3)
            and 'dual_verification' in previous, 'checkpoint must be a preceding dual QA receipt')
    dual=previous['dual_verification']
    art=dual['artistic']
    require(isinstance(art,dict), 'checkpoint needs a completed artistic review')
    validation=evaluate(dual,previous,root=root,verify_artifact=verify_artifact,_depth=_depth+1)
    images={x['id']:x for x in previous['captures']+previous['closeups']}
    bindings={x['id']:x for x in dual['freshness']['captures']}
    checkpoint=copy.deepcopy(dual['checkpoint'])
    checkpoint['artifact']=copy.deepcopy(artifact)
    checkpoint['issues']=[dict(id=x['id'],region=x['where'],evidence=sorted({images[cid]['image']['sha256'] for cid in x['evidence']})) for x in art['issues']]
    for region in art['preserve']+art['leave_as_is']:
        if region not in dual['brief']['requirements'] or fresh.sufficient(
                {region:dual['brief']['requirements'][region]},
                {cid:images[cid] for cid in art['inspected']}, validation['freshness'])['status']!='SUFFICIENT':
            continue
        hashes=sorted({images[cid]['image']['sha256'] for cid in art['inspected']
                       if region in bindings.get(cid,{}).get('dependencies',{})})
        if hashes:
            checkpoint['accepted'][region]=hashes
    checkpoint['protected']=sorted(set(checkpoint['protected']) | set(dual['brief']['protected']))
    failures={}
    failed=set(checkpoint['failed_methods'])
    for row in dual['corrections']:
        method=row['method'].strip().casefold()
        for iid,outcome in row['outcomes'].items():
            prev=failures.get(iid,('',0))
            failures[iid]=(method,prev[1]+1 if prev[0]==method else 1) if outcome=='UNRESOLVED' else ('',0)
            if failures[iid][1]>=2:
                failed.add(method)
    checkpoint['failed_methods']=sorted(failed)
    if validation['artistic_gate']=='PASS' and dual['brief']['scope']=='FULL' and art['verdict'] in ('ACCEPTED','ACCEPTED_WITH_MINOR_DIFFERENCES'):
        # Minor differences close a checkpoint only after the user's FINISH choice.
        if art['verdict']=='ACCEPTED' or dual['user_decision']=='FINISH':
            checkpoint['gates'][art['stage']]=dict(verdict='ACCEPTED',contract_ref=dual['brief']['contract']['ref'],
                            evidence=art['inspected'],reviewer=art['reviewer'],packet_sha256=art['packet_sha256'])
    return checkpoint


def correction_decision(verdict, corrections, issues, *, user_decision='PENDING', protected=()):
    """No mutation; return the permitted next action for one bounded correction batch."""
    require(verdict in VERDICTS and user_decision in ('PENDING','FINISH','POLISH'), 'invalid correction verdict/choice')
    require(isinstance(corrections, list) and len(corrections) <= 3, 'at most three correction passes')
    failures = {}
    for number, row in enumerate(corrections, 1):
        exact(row, ('pass','method','outcomes','checkpoint','evidence'), 'correction pass')
        require(type(row['pass']) is int and row['pass'] == number and isinstance(row['method'], str) and row['method'].strip(),
                'correction passes must be contiguous with a named method')
        require(isinstance(row['outcomes'], dict) and row['outcomes'] and
                all(isinstance(k,str) and k.strip() and v in ('RESOLVED','IMPROVED','UNRESOLVED') for k,v in row['outcomes'].items()),
                'correction outcomes required')
        method = row['method'].strip().casefold()
        for issue, outcome in row['outcomes'].items():
            previous = failures.get(issue, ('',0))
            require(previous != (method,2), 'same method repeated after two unsuccessful corrections')
            failures[issue] = (method, previous[1]+1 if previous[0]==method else 1) if outcome=='UNRESOLVED' else ('',0)
    if verdict == 'ESCALATE' or any(x['where'] in protected for x in issues):
        return 'ESCALATE'
    if verdict == 'ACCEPTED':
        return 'FINISH'
    if verdict == 'ACCEPTED_WITH_MINOR_DIFFERENCES':
        if user_decision == 'POLISH' and any(failures.get(x['id'], ('',0))[1] >= 2 for x in issues):
            return 'RECONSIDER_METHOD'
        return 'USER_DECISION' if user_decision=='PENDING' else 'FINISH' if user_decision=='FINISH' else 'CORRECT' if len(corrections)<3 else 'ESCALATE'
    if len(corrections) == 3:
        return 'ESCALATE'
    if any(failures.get(x['id'], ('',0))[1] >= 2 for x in issues):
        return 'RECONSIDER_METHOD'
    return 'CORRECT'


def evaluate(record, packet, *, root, verify_artifact, _depth=0):
    require(_depth <= 16, 'checkpoint chain exceeds bounded review history; archive and explicitly rebaseline')
    exact(record, ('version','freshness','technical_checks','brief','artistic','checkpoint','corrections','user_decision'), 'dual verification')
    require(type(record['version']) is int and record['version']==1, 'unsupported dual verification version')
    images = {x['id']:x for x in packet['captures']+packet['closeups']}
    require({x['id'] for x in packet['protected_zones']} | {x['id'] for x in packet['user_flags']
            if x['action'] in ('PRESERVE','DO_NOT_REINTERPRET')} <= set(record['brief']['protected']),
            'receipt protected zones/user locks omitted from critic brief')
    freshness = fresh.assess(record['freshness'], images, root=root, verify_artifact=verify_artifact)
    if record['brief']['scope']=='LOCAL':
        affected=set().union(*(set(row['changed_regions']) | {r for r,s in row['regions'].items() if s=='PARTIAL'} for row in freshness.values()))
        require(affected & set(record['brief']['protected']) <= set(record['brief']['requirements']),
                'local review omitted affected protected region')
    names = record['technical_checks']
    strings(names, 'technical check names', nonempty=True)
    checks = packet['checks']
    technical = ('FAIL' if any(checks.get(x, {}).get('status')=='FAIL' for x in names) else
                 'PASS' if root is not None and all(checks.get(x, {}).get('status')=='PASS' for x in names) else 'OPEN')
    out = dict(TECHNICAL_QA=technical, technical_scope=names, ARTISTIC_REVIEW='NOT_REVIEWED', artistic_gate='OPEN',
               independence='NOT_RECORDED', freshness=freshness, requests=[], delta=[], next='REQUEST_REVIEW',
               critic_packet=None, packet_sha256=None, limits='Declared review evidence only; checker does not see pixels or attest agent dispatch.')
    if root is None:
        out['next']='VERIFY_FILES'
        return out
    checkpoint = record['checkpoint']
    exact(checkpoint, ('artifact','issues','accepted','protected','failed_methods','gates'), 'review checkpoint')
    previous_corrections=[]
    historical_images={}
    has_history=any(checkpoint[x] for x in ('issues','accepted','failed_methods','gates'))
    if has_history or checkpoint['artifact'] is not None:
        require(checkpoint['artifact'] is not None, 'previous critic state requires its existing QA receipt checkpoint')
        verify_artifact(checkpoint['artifact'], 'previous QA receipt', root, png_only=False)
        previous_packet=json.loads((Path(root)/checkpoint['artifact']['path']).read_text(encoding='utf-8-sig'))
        require(checkpoint_from_receipt(previous_packet,checkpoint['artifact'],root=root,verify_artifact=verify_artifact,_depth=_depth) == checkpoint,
                'checkpoint memory differs from preceding QA receipt')
        require(previous_packet['dual_verification']['brief']['contract']['ref']==record['brief']['contract']['ref'], 'checkpoint contract changed')
        previous_corrections=previous_packet['dual_verification']['corrections']
        historical_images={x['id']:x for x in previous_packet['captures']+previous_packet['closeups']}
        for cid, image in historical_images.items():
            if image['image'] is not None:
                verify_artifact(image['image'], 'checkpoint image '+cid, root)
                fresh.png_integrity(Path(root)/image['image']['path'])
        require(record['corrections'][:len(previous_corrections)]==previous_corrections, 'previous correction attempts cannot be removed/changed')
        for row in record['corrections'][len(previous_corrections):]:
            require(row['method'].strip().casefold() not in {x.strip().casefold() for x in checkpoint['failed_methods']},
                    'known failed method requires reconsideration before another pass')
    objective = critic_packet(record['brief'],images,freshness,root=root,verify_artifact=verify_artifact,accepted=checkpoint['accepted'])
    objective_hash = fresh.digest(objective)
    out.update(critic_packet=objective, packet_sha256=objective_hash, requests=objective['sufficiency']['requests'])
    strings(checkpoint['protected'], 'checkpoint protected')
    strings(checkpoint['failed_methods'], 'failed methods')
    require(set(checkpoint['protected']) <= set(record['brief']['protected']), 'protected zones silently dropped')
    require(isinstance(checkpoint['gates'], dict) and set(checkpoint['gates']) <= set(GATES[record['brief']['complexity']]), 'invalid completed gates')
    for gate, receipt in checkpoint['gates'].items():
        exact(receipt, ('verdict','contract_ref','evidence','reviewer','packet_sha256'), 'completed artistic gate')
        require(receipt['verdict'] in VERDICTS and receipt['contract_ref']==record['brief']['contract']['ref']
                and isinstance(receipt['reviewer'],str) and receipt['reviewer'].strip()
                and isinstance(receipt['packet_sha256'],str) and len(receipt['packet_sha256'])==64
                and all(c in '0123456789abcdef' for c in receipt['packet_sha256']),
                'invalid/stale previous gate verdict/contract')
        strings(receipt['evidence'], 'previous gate capture IDs', nonempty=True)
        require(all(cid in historical_images and historical_images[cid]['phase']=='AFTER'
                    and historical_images[cid]['status'] in ('PASS','WARN') for cid in receipt['evidence']),
                'previous gate needs reviewed file-verified images')
    if checkpoint['artifact'] is not None:
        verify_artifact(checkpoint['artifact'], 'checkpoint', root, png_only=False)
    require(isinstance(checkpoint['issues'], list) and isinstance(checkpoint['accepted'], dict), 'checkpoint issues/accepted required')
    previous = {}
    for row in checkpoint['issues']:
        exact(row, ('id','region','evidence'), 'previous issue')
        require(isinstance(row['id'], str) and row['id'].strip() and row['id'] not in previous
                and isinstance(row['region'],str) and row['region'].strip(), 'invalid previous issue')
        strings(row['evidence'], 'previous evidence hashes', nonempty=True)
        previous[row['id']] = row
    for region, hashes in checkpoint['accepted'].items():
        require(isinstance(region,str) and region.strip(), 'invalid accepted region')
        strings(hashes, 'accepted evidence hashes', nonempty=True)
        require(all(len(x)==64 and all(c in '0123456789abcdef' for c in x) for x in hashes), 'accepted PNG hash required')
    # Checkpoints are evidence pointers, never a second design authority.
    for row in record['corrections']:
        verify_artifact(row['checkpoint'], 'correction checkpoint', root, png_only=False)
        require(row['checkpoint']['path'].lower().endswith('.blend'), 'correction needs saved Blender checkpoint')
        strings(row['evidence'], 'correction AFTER evidence', nonempty=True)
        relevant_images = historical_images if row['pass'] <= len(previous_corrections) else images
        require(all(cid in relevant_images and relevant_images[cid]['phase']=='AFTER' for cid in row['evidence']), 'correction needs AFTER images')
    art = record['artistic']
    if art is None:
        require(len(record['corrections']) <= 3, 'at most three correction passes')
        out['next'] = 'REQUEST_CAPTURE' if out['requests'] else 'REQUEST_REVIEW'
        return out
    exact(art, ('stage','verdict','mode','reviewer','packet_sha256','dispatch','inspected',
                'issues','delta','preserve','leave_as_is','do_not_change','next','observations'), 'artistic review')
    require(art['verdict'] in VERDICTS and art['stage']==record['brief']['stage'] and art['packet_sha256']==objective_hash,
            'stale or changed critic packet/contract/stage')
    strings(art['inspected'], 'inspected capture IDs', nonempty=True)
    require(set(art['inspected']) <= set(images), 'unknown inspected image')
    for field in ('preserve','leave_as_is','do_not_change','next'):
        strings(art[field], 'artistic '+field)
    require(isinstance(art['reviewer'], str) and art['reviewer'].strip() and isinstance(art['observations'], str)
            and art['observations'].strip(), 'critic observations/reviewer required')
    require(set(record['brief']['protected']) <= set(art['do_not_change']), 'critic must retain protected zones')
    require(set(checkpoint['accepted']) <= set(art['preserve']) | set(art['leave_as_is']) | {x['where'] for x in art['issues']},
            'accepted regions silently dropped from critic preservation plan')
    if art['mode']=='SELF_REVIEW':
        require(art['reviewer']==record['brief']['implementer'] and art['dispatch'] is None, 'false SELF_REVIEW identity')
    else:
        require(art['mode']=='INDEPENDENT' and art['reviewer']!=record['brief']['implementer'] and art['dispatch'] is not None,
                'independent critic must be a different dispatched agent')
        verify_artifact(art['dispatch'], 'critic dispatch receipt', root, png_only=False)
        dispatch = json.loads((Path(root)/art['dispatch']['path']).read_text(encoding='utf-8-sig'))
        exact(dispatch, ('implementer','critic','dispatch_id','packet_sha256','blind'), 'critic dispatch')
        require(dispatch['implementer']==record['brief']['implementer'] and dispatch['critic']==art['reviewer']
                and isinstance(dispatch['dispatch_id'], str) and dispatch['dispatch_id'].strip()
                and dispatch['packet_sha256']==objective_hash and dispatch['blind'] is True, 'unbound/nonblind critic dispatch')
    out['independence'] = art['mode'] + ('_DECLARED' if art['mode']=='INDEPENDENT' else '')
    inspected_coverage = fresh.sufficient(record['brief']['requirements'],
                                         {cid:images[cid] for cid in art['inspected']}, freshness)
    if inspected_coverage['requests']:
        missing_actual={(x['region'],x['view']) for x in objective['sufficiency']['requests']}
        out['requests'] = [dict(x,action='REQUEST_CAPTURE' if (x['region'],x['view']) in missing_actual else 'INSPECT_EXISTING')
                           for x in inspected_coverage['requests']]
    require(isinstance(art['issues'], list) and len(art['issues']) <= 5, 'at most five critic issues')
    issue_ids = set()
    for issue in art['issues']:
        exact(issue, ('id','priority','what','where','why','evidence','reference','fix','kind','visibility',
                      'impact','fix_cost','regression_risk','rationale'), 'critic issue')
        require(isinstance(issue['id'],str) and issue['id'].strip() and issue['id'] not in issue_ids
                and issue['priority'] in ('P0','P1','P2') and issue['where'] in record['brief']['requirements'], 'invalid critic issue identity/region/priority')
        issue_ids.add(issue['id'])
        require(all(isinstance(issue[f],str) and issue[f].strip() for f in ('what','why','fix','rationale')),
                'issue WHAT/WHY/FIX/cost rationale required')
        require(all(issue[f] in ('LOW','MEDIUM','HIGH') for f in ('impact','fix_cost','regression_risk')), 'invalid impact/cost/risk')
        require(issue['kind'] in ('PROPORTION','FORM','CONTACT','SURFACE','MISSING')
                and issue['visibility'] in ('VISIBLE','PARTIAL','OCCLUDED'), 'invalid issue kind/visibility')
        strings(issue['evidence'], 'issue evidence', nonempty=True)
        require(set(issue['evidence']) <= set(art['inspected']) and issue['reference'] in record['brief']['references'], 'issue needs inspected images and canonical reference')
        require(all(freshness.get(cid, {}).get('regions', {}).get(issue['where'])=='CURRENT' for cid in issue['evidence']),
                'issue cannot rely on stale/partial/unknown region evidence')
        views = {images[cid].get('view') for cid in issue['evidence'] if images[cid]['setup']['projection']=='ORTHO'}
        require(issue['kind']!='PROPORTION' or {'front','side'} <= views, '45-degree views cannot establish proportions; confirm front and side')
        require(issue['kind']!='MISSING' or issue['visibility']=='VISIBLE', 'occluded does not mean absent; request unobstructed evidence')
        hashes = {images[cid]['image']['sha256'] for cid in issue['evidence']}
        old = checkpoint['accepted'].get(issue['where'], [])
        require(not old or hashes-set(old), 'accepted region cannot return to correction without new evidence')
    require(art['verdict']!='ACCEPTED' or not art['issues'], 'ACCEPTED must have zero unresolved issues')
    require(art['verdict']!='ACCEPTED_WITH_MINOR_DIFFERENCES' or all(x['priority']=='P2' and x['impact']=='LOW' for x in art['issues']),
            'minor verdict cannot hide a major deviation')
    require(art['verdict']!='REVISION_REQUIRED' or art['issues'], 'revision verdict needs a confirmed defect')
    require(isinstance(art['delta'], list), 'critic delta required')
    delta_ids=set()
    for delta in art['delta']:
        exact(delta, ('id','status','evidence'), 'critic delta')
        require(delta['id'] not in delta_ids and delta['status'] in ('RESOLVED','IMPROVED','UNRESOLVED','NEW_REGRESSION'), 'invalid duplicate delta')
        delta_ids.add(delta['id'])
        require(delta['id'] in previous or delta['id'] in issue_ids, 'unknown delta issue')
        require((delta['status']=='RESOLVED') == (delta['id'] not in issue_ids), 'resolved delta contradicts outstanding issue')
        require(delta['status'] not in ('IMPROVED','UNRESOLVED') or delta['id'] in previous, 'improvement needs previous issue')
        strings(delta['evidence'], 'delta inspected evidence', nonempty=True)
        region = previous[delta['id']]['region'] if delta['id'] in previous else next(x['where'] for x in art['issues'] if x['id']==delta['id'])
        require(all(cid in art['inspected'] and freshness.get(cid,{}).get('regions',{}).get(region)=='CURRENT' for cid in delta['evidence']), 'delta needs current inspected evidence')
        if delta['status'] in ('RESOLVED','IMPROVED','NEW_REGRESSION') and delta['id'] in previous:
            require({images[cid]['image']['sha256'] for cid in delta['evidence']}-set(previous[delta['id']]['evidence']), 'delta needs new evidence')
    require(set(previous) <= delta_ids, 'previous defects cannot silently disappear')
    for issue in art['issues']:
        if issue['where'] in checkpoint['accepted']:
            require(any(x['id']==issue['id'] and x['status']=='NEW_REGRESSION' for x in art['delta']), 'accepted-region defect must be tracked as new regression')
    decision = correction_decision(art['verdict'], record['corrections'], art['issues'],
                                   user_decision=record['user_decision'], protected=record['brief']['protected'])
    state_reviews={}
    for correction in record['corrections']:
        if correction['pass'] <= len(previous_corrections):
            continue  # Immutable prefix from the bound receipt; don't reopen resolved issues.
        regions = {next((x['where'] for x in art['issues'] if x['id']==iid), previous.get(iid,{}).get('region')) for iid in correction['outcomes']}
        require(None not in regions, 'correction outcomes must bind to tracked issue regions')
        # Historical AFTER images may be stale now; the latest verdict must use
        # current evidence. File integrity for all correction images is still mandatory.
        require(all(freshness.get(cid,{}).get('image_integrity')=='PASS' for cid in correction['evidence']), 'correction images not verified')
        bindings={x['id']:x for x in record['freshness']['captures']}
        require(all(any(r in bindings[cid]['dependencies'] and bindings[cid]['dependencies'][r] is not None
                        for cid in correction['evidence']) for r in regions), 'correction needs evidence of each affected region')
        for cid in correction['evidence']:
            state=bindings[cid]['state']
            if state not in state_reviews:
                captured_record=dict(record['freshness'], current=state)
                state_reviews[state]=fresh.assess(captured_record,images,root=root,verify_artifact=verify_artifact)
        require(all(any(state_reviews[bindings[cid]['state']][cid]['regions'].get(r)=='CURRENT'
                        for cid in correction['evidence']) for r in regions), 'correction needs verified region state at its AFTER capture')
        if correction['pass']==len(record['corrections']):
            require(all(any(freshness[cid]['regions'].get(r)=='CURRENT' for cid in correction['evidence']) for r in regions),
                    'latest correction AFTER evidence is stale/unknown')
        require(all(images[cid]['status'] in ('PASS','WARN') for cid in correction['evidence']), 'correction evidence must be inspected')
        for iid, outcome in correction['outcomes'].items():
            if outcome in ('RESOLVED','IMPROVED'):
                region=next((x['where'] for x in art['issues'] if x['id']==iid), previous.get(iid,{}).get('region'))
                earlier = next((row for row in record['corrections'] if row['pass']==correction['pass']-1), None)
                prior_images = historical_images if earlier and earlier['pass'] <= len(previous_corrections) else images
                prior_bindings={x['id']:x for x in previous_packet['dual_verification']['freshness']['captures']} if earlier and earlier['pass']<=len(previous_corrections) else bindings
                old_hashes = {prior_images[cid]['image']['sha256'] for cid in earlier['evidence'] if region in prior_bindings[cid]['dependencies']} if earlier else set(previous.get(iid,{}).get('evidence',[]))
                new_hashes = {images[cid]['image']['sha256'] for cid in correction['evidence'] if region in bindings[cid]['dependencies']}
                require(old_hashes and new_hashes-old_hashes,
                        'improvement/resolution needs new region evidence relative to preceding pass/issue')
                if correction['pass']==len(record['corrections']):
                    require(any(d['id']==iid and d['status']==outcome for d in art['delta']),
                            'latest correction improvement/resolution needs matching critic delta')
    prior = GATES[record['brief']['complexity']]
    missing_gates = [] if record['brief']['scope']=='LOCAL' else [g for g in prior[:prior.index(art['stage'])]
        if checkpoint['gates'].get(g, {}).get('verdict') != 'ACCEPTED']
    out.update(ARTISTIC_REVIEW=art['verdict'], delta=copy.deepcopy(art['delta']), next=decision)
    if out['requests']:
        out.update(artistic_gate='OPEN', next='REQUEST_CAPTURE' if any(x['action']=='REQUEST_CAPTURE' for x in out['requests']) else 'INSPECT_EXISTING')
    elif missing_gates:
        out.update(artistic_gate='OPEN', next='REVIEW_MISSING_GATES', missing_gates=missing_gates)
    else:
        out['artistic_gate'] = 'PASS' if decision=='FINISH' else 'FAIL' if art['verdict'] in ('REVISION_REQUIRED','ESCALATE') or decision=='ESCALATE' else 'OPEN'
    return out
