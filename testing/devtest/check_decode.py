# check we decoded the PSBT correctly, by looking under the covers.
import main
expect = main.EXPECT

from auth import active_request, ApproveTransaction
assert isinstance(active_request, ApproveTransaction)

assert not active_request.failed, active_request.failed
assert not active_request.refused, 'refused'

p = active_request.psbt
assert p, "state confused; retry?"

p.validate()
p.validate()

for fn in ['had_witness', 'num_inputs', 'num_outputs',
            'lock_time', 'total_value_out', 'total_value_in']:

    val = getattr(p, fn, 'MISSING')

    #print("%s = %r" % (fn, val))

    if fn not in expect:
        continue

    assert expect[fn] == val, "%s: expected %r, got %r" % (fn, expect[fn], val)

# check outputs: amt and dest addr
for (val, addr), (idx, txo) in zip(expect['destinations'], p.output_iter()):
    assert val == txo.nValue
    txt = active_request.render_output(txo)
    assert addr in txt
    assert '%.8f'%(val/1E8) in txt

change_set = set()
for n in range(len(p.outputs)):
     if p.outputs[n].is_change:
        change_set.add(n)

if 'change_outs' in expect:
    assert expect['change_outs'] == change_set, change_set

assert expect['miner_fee'] == p.calculate_fee()
assert expect['warnings_expected'] == len(p.warnings), repr(p.warnings)
