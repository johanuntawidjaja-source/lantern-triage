let model;
const $=s=>document.querySelector(s);
const labels={TEMPERATURE_EXCURSION:"Temperature excursion",DAMAGE:"Damage",DELAY:"Delay",WRONG_DESTINATION:"Wrong destination",DOCUMENTATION:"Documentation",CUSTOMS_HOLD:"Customs hold",OTHER:"Other",HUMAN_REVIEW:"Human review"};
const tokenize=t=>{const words=t.toLowerCase().match(/[a-z0-9]+/g)||[],f=[...words];for(let i=0;i<words.length-1;i++)f.push(`w2:${words[i]}_${words[i+1]}`);for(const word of words){const p=`^${word}$`;for(const n of [3,4,5])for(let i=0;i<=p.length-n;i++)f.push(`c:${p.slice(i,i+n)}`)}return f};
function predict(text){
  const words=tokenize(text), scores={};
  for(const label of model.labels){let score=Math.log(model.priors[label]),den=model.totals[label]+model.vocabSize;for(const w of words)score+=Math.log(((model.counts[label][w]||0)+1)/den);scores[label]=score}
  const peak=Math.max(...Object.values(scores)),temperature=model.temperature||2,raw=Object.fromEntries(Object.entries(scores).map(([k,v])=>[k,Math.exp((v-peak)/temperature)])),z=Object.values(raw).reduce((a,b)=>a+b,0),probs=Object.fromEntries(Object.entries(raw).map(([k,v])=>[k,v/z]));
  const lower=text.toLowerCase(),category=Object.keys(probs).sort((a,b)=>probs[b]-probs[a])[0],confidence=probs[category],urgent=category==="TEMPERATURE_EXCURSION"||model.urgentTerms.some(t=>lower.includes(t)),genericOnly=(model.ambiguousPhrases||[]).some(t=>lower.includes(t))&&!(model.categoryAnchors||[]).some(t=>lower.includes(t)),abstain=confidence<model.threshold||genericOnly;
  return {category,route:abstain?"HUMAN_REVIEW":category,confidence,urgent,abstain,abstainReason:genericOnly?"ambiguous_language":(confidence<model.threshold?"low_confidence":null),probs};
}
function render(p){
  $("#empty").hidden=true;$("#result").hidden=false;$("#route").textContent=labels[p.route];$("#confidence").textContent=p.abstainReason==="ambiguous_language"?"Ambiguous input":`${Math.min(99,Math.round(p.confidence*100))}% model confidence`;
  $("#urgent").textContent=p.urgent?"Urgent language detected — prioritize human attention":"No explicit urgent language detected";
  $("#explanation").textContent=p.abstainReason==="ambiguous_language"?"The report is too general to identify an operational problem safely.":p.abstain?"The model is not confident enough to force an operational queue.":`The report's word and character patterns most closely match the ${labels[p.category].toLowerCase()} examples in the training set.`;
  $("#next").textContent=p.abstain?"A dispatcher should review the original report and choose the queue.":`Send to ${labels[p.category]} for confirmation. A human remains accountable for the final route.`;
  $("#probabilities").innerHTML=Object.entries(p.probs).sort((a,b)=>b[1]-a[1]).map(([k,v])=>`<div class="bar"><span>${labels[k]}</span><span class="track"><span class="fill" style="display:block;width:${v*100}%"></span></span><b>${Math.round(v*100)}%</b></div>`).join("");
}
async function init(){model=await fetch("model.json").then(r=>r.json());try{const r=await fetch("evaluation/results.json").then(r=>r.json());$("#coverage").textContent=`${Math.round(r[1].coverage*100)}%`}catch{$("#coverage").textContent="Measured"}}
$("#classify").onclick=()=>{const text=$("#report").value.trim();if(!text){$("#report").focus();return}render(predict(text))};
$("#example").onclick=()=>{$("#report").value="Customs placed a refrigerated medicine shipment on hold pending inspection. Clearance is required today.";render(predict($("#report").value))};
$("#clear").onclick=()=>{$("#report").value="";$("#result").hidden=true;$("#empty").hidden=false};
init().catch(()=>{$("#empty").textContent="Model failed to load. Serve this folder over HTTP; see README."});

