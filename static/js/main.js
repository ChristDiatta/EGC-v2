/* EGC Ingénierie : interactions & animations */
(() => {
    'use strict';

    const $ = (sel, root = document) => root.querySelector(sel);
    const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    /* ------------------------------------------------------------------ */
    /* Loader                                                              */
    /* ------------------------------------------------------------------ */
    const loader = $('#loader');
    const hideLoader = () => loader && loader.classList.add('is-hidden');
    window.addEventListener('load', () => setTimeout(hideLoader, 350));
    setTimeout(hideLoader, 3000); // filet de sécurité si une ressource externe traîne

    /* ------------------------------------------------------------------ */
    /* Menu mobile                                                         */
    /* ------------------------------------------------------------------ */
    const menuBtn = $('#mobile-menu-btn');
    const mobileMenu = $('#mobile-menu');

    const setMenu = (open) => {
        mobileMenu.classList.toggle('is-open', open);
        menuBtn.setAttribute('aria-expanded', String(open));
        const icon = $('i', menuBtn);
        icon.classList.toggle('fa-bars', !open);
        icon.classList.toggle('fa-xmark', open);
    };
    menuBtn.addEventListener('click', () => setMenu(!mobileMenu.classList.contains('is-open')));
    $$('.mobile-link').forEach((l) => l.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', (e) => e.key === 'Escape' && setMenu(false));

    /* ------------------------------------------------------------------ */
    /* Scroll : progression, navbar, retour en haut, parallaxe             */
    /* ------------------------------------------------------------------ */
    const navbar = $('#navbar');
    const progress = $('#scroll-progress');
    const toTop = $('#back-to-top');
    const parallax = $$('[data-parallax]');
    let ticking = false;

    const onScroll = () => {
        const y = window.scrollY;
        const max = document.documentElement.scrollHeight - window.innerHeight;
        progress.style.transform = `scaleX(${max > 0 ? Math.min(y / max, 1) : 0})`;
        navbar.classList.toggle('nav-scrolled', y > 50);
        toTop.classList.toggle('is-show', y > 700);
        if (!reduceMotion && y < window.innerHeight * 1.5) {
            parallax.forEach((el) => {
                el.style.translate = `0 ${y * parseFloat(el.dataset.parallax)}px`;
            });
        }
        ticking = false;
    };
    window.addEventListener('scroll', () => {
        if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
    }, { passive: true });
    onScroll();

    toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

    /* ------------------------------------------------------------------ */
    /* Scrollspy : lien actif dans la navigation                           */
    /* ------------------------------------------------------------------ */
    const spyLinks = $$('.nav-link');
    const sections = spyLinks
        .map((a) => document.getElementById(a.dataset.spy))
        .filter(Boolean);

    if (sections.length) {
        const spy = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                spyLinks.forEach((a) => {
                    const active = a.dataset.spy === entry.target.id;
                    a.classList.toggle('is-active', active);
                    a.classList.toggle('text-white', active);
                    a.classList.toggle('text-egc-muted', !active);
                });
            });
        }, { rootMargin: '-45% 0px -50% 0px' });
        sections.forEach((s) => spy.observe(s));
    }

    /* ------------------------------------------------------------------ */
    /* Révélation au scroll                                                */
    /* ------------------------------------------------------------------ */
    const revealEls = $$('[data-reveal]');
    revealEls.forEach((el) => {
        const delay = parseInt(el.dataset.delay || '0', 10);
        el.style.setProperty('--d', `${delay}ms`);
    });

    if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries, obs) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
        revealEls.forEach((el) => io.observe(el));
    } else {
        revealEls.forEach((el) => el.classList.add('is-visible'));
    }

    /* ------------------------------------------------------------------ */
    /* Compteurs animés                                                    */
    /* ------------------------------------------------------------------ */
    const counters = $$('[data-count]');
    const easeOut = (t) => 1 - Math.pow(1 - t, 4);

    const runCounter = (el) => {
        const target = parseInt(el.dataset.count, 10);
        const suffix = el.dataset.suffix || '';
        const duration = 1800;
        const start = performance.now();
        const step = (now) => {
            const t = Math.min((now - start) / duration, 1);
            el.textContent = Math.round(target * easeOut(t)) + suffix;
            if (t < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
    };

    if (!reduceMotion && 'IntersectionObserver' in window) {
        counters.forEach((el) => { el.textContent = '0' + (el.dataset.suffix || ''); });
        const cio = new IntersectionObserver((entries, obs) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) return;
                runCounter(entry.target);
                obs.unobserve(entry.target);
            });
        }, { threshold: 0.6 });
        counters.forEach((el) => cio.observe(el));
    }

    /* ------------------------------------------------------------------ */
    /* Halo qui suit le curseur (cartes)                                   */
    /* ------------------------------------------------------------------ */
    if (finePointer) {
        $$('.glass-card-hover, .spotlight').forEach((card) => {
            card.addEventListener('pointermove', (e) => {
                const r = card.getBoundingClientRect();
                card.style.setProperty('--mx', `${e.clientX - r.left}px`);
                card.style.setProperty('--my', `${e.clientY - r.top}px`);
            });
        });
    }

    /* ------------------------------------------------------------------ */
    /* Inclinaison 3D + boutons magnétiques                                */
    /* ------------------------------------------------------------------ */
    if (finePointer && !reduceMotion) {
        $$('[data-tilt]').forEach((el) => {
            el.addEventListener('pointermove', (e) => {
                const r = el.getBoundingClientRect();
                const px = (e.clientX - r.left) / r.width - 0.5;
                const py = (e.clientY - r.top) / r.height - 0.5;
                el.style.transform =
                    `perspective(1000px) rotateX(${(-py * 8).toFixed(2)}deg) rotateY(${(px * 10).toFixed(2)}deg)`;
            });
            el.addEventListener('pointerleave', () => { el.style.transform = ''; });
        });

        $$('.magnetic').forEach((btn) => {
            btn.addEventListener('pointermove', (e) => {
                const r = btn.getBoundingClientRect();
                const dx = (e.clientX - (r.left + r.width / 2)) * 0.18;
                const dy = (e.clientY - (r.top + r.height / 2)) * 0.28;
                btn.style.transform = `translate(${dx.toFixed(1)}px, ${dy.toFixed(1)}px)`;
            });
            btn.addEventListener('pointerleave', () => { btn.style.transform = ''; });
        });
    }

    /* Ondulation au clic */
    $$('.btn-fx').forEach((btn) => {
        btn.addEventListener('pointerdown', (e) => {
            if (reduceMotion) return;
            const r = btn.getBoundingClientRect();
            const size = Math.max(r.width, r.height);
            const span = document.createElement('span');
            span.className = 'ripple';
            span.style.width = span.style.height = `${size}px`;
            span.style.left = `${e.clientX - r.left - size / 2}px`;
            span.style.top = `${e.clientY - r.top - size / 2}px`;
            btn.appendChild(span);
            span.addEventListener('animationend', () => span.remove());
        });
    });

    /* ------------------------------------------------------------------ */
    /* Réseau de particules (hero)                                         */
    /* ------------------------------------------------------------------ */
    const canvas = $('#particles');
    if (canvas && !reduceMotion) {
        const ctx = canvas.getContext('2d');
        const hero = canvas.parentElement;
        const mouse = { x: -9999, y: -9999 };
        let w = 0, h = 0, dpr = 1, particles = [], running = false, raf = 0;

        const resize = () => {
            dpr = Math.min(window.devicePixelRatio || 1, 2);
            w = hero.clientWidth;
            h = hero.clientHeight;
            canvas.width = w * dpr;
            canvas.height = h * dpr;
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            const count = Math.min(Math.floor((w * h) / 16000), 70);
            particles = Array.from({ length: count }, () => ({
                x: Math.random() * w,
                y: Math.random() * h,
                vx: (Math.random() - 0.5) * 0.35,
                vy: (Math.random() - 0.5) * 0.35,
                r: Math.random() * 1.4 + 0.6,
                green: Math.random() > 0.72,
            }));
        };

        const LINK = 130;
        const frame = () => {
            ctx.clearRect(0, 0, w, h);
            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0 || p.x > w) p.vx *= -1;
                if (p.y < 0 || p.y > h) p.vy *= -1;

                const mdx = p.x - mouse.x, mdy = p.y - mouse.y;
                const md = Math.hypot(mdx, mdy);
                if (md < 120) { p.x += (mdx / md) * 0.8; p.y += (mdy / md) * 0.8; }

                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = p.green ? 'rgba(34,197,94,0.75)' : 'rgba(0,210,255,0.75)';
                ctx.fill();

                for (let j = i + 1; j < particles.length; j++) {
                    const q = particles[j];
                    const d = Math.hypot(p.x - q.x, p.y - q.y);
                    if (d < LINK) {
                        ctx.strokeStyle = `rgba(0,210,255,${(1 - d / LINK) * 0.18})`;
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(q.x, q.y);
                        ctx.stroke();
                    }
                }
            }
            raf = requestAnimationFrame(frame);
        };

        const start = () => { if (!running) { running = true; raf = requestAnimationFrame(frame); } };
        const stop = () => { running = false; cancelAnimationFrame(raf); };

        resize();
        window.addEventListener('resize', resize);
        hero.addEventListener('pointermove', (e) => {
            const r = hero.getBoundingClientRect();
            mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
        });
        hero.addEventListener('pointerleave', () => { mouse.x = mouse.y = -9999; });

        // Pause quand le hero n'est plus visible (économie CPU/batterie)
        new IntersectionObserver(([e]) => (e.isIntersecting ? start() : stop())).observe(hero);
        document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    }

    /* ------------------------------------------------------------------ */
    /* Formulaire de devis (AJAX)                                          */
    /* ------------------------------------------------------------------ */
    const form = $('#contact-form');
    const successBox = $('#success-message');
    const successText = $('#success-text');
    const submitBtn = $('#submit-btn');
    const toast = $('#toast');
    let toastTimer, successTimer;

    if (form) {

    const showToast = (msg, ok = false) => {
        toast.textContent = msg;
        toast.classList.toggle('is-ok', ok);
        toast.classList.add('is-show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toast.classList.remove('is-show'), 4500);
    };

    const clearErrors = () => {
        $$('.field.has-error', form).forEach((f) => f.classList.remove('has-error'));
        $$('.field-error', form).forEach((p) => { p.textContent = ''; });
    };

    const setError = (name, message) => {
        const p = $(`[data-error-for="${name}"]`, form);
        if (!p) return;
        p.textContent = message;
        const field = p.closest('.field');
        // Relance l'animation "shake" même si le champ était déjà en erreur
        field.classList.remove('has-error');
        void field.offsetWidth;
        field.classList.add('has-error');
    };

    // Retire l'erreur dès que l'utilisateur corrige
    form.addEventListener('input', (e) => {
        const field = e.target.closest('.field');
        if (field) field.classList.remove('has-error');
    });

    // Validation côté client (miroir de celle du serveur)
    const clientValidate = (d) => {
        const errs = {};
        if (d.name.trim().length < 2) errs.name = 'Veuillez indiquer votre nom complet.';
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(d.email.trim())) errs.email = 'Adresse e-mail invalide.';
        if (d.phone.replace(/\D/g, '').length < 8) errs.phone = 'Numéro de téléphone invalide.';
        if (!d.lots.length) errs.lots = 'Sélectionnez au moins un lot technique.';
        if (d.message.trim().length < 10) errs.message = 'Décrivez brièvement votre projet (10 caractères min.).';
        return errs;
    };

    const setLoading = (loading) => {
        submitBtn.disabled = loading;
        submitBtn.classList.toggle('is-loading', loading);
        $('.btn-label', submitBtn).textContent = loading ? 'Envoi en cours…' : 'Envoyer ma demande de devis';
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearErrors();

        const fd = new FormData(form);
        const payload = {
            name: fd.get('name') || '',
            company: fd.get('company') || '',
            email: fd.get('email') || '',
            phone: fd.get('phone') || '',
            lots: fd.getAll('lots'),
            message: fd.get('message') || '',
            website: fd.get('website') || '',
        };

        const errs = clientValidate(payload);
        if (Object.keys(errs).length) {
            Object.entries(errs).forEach(([k, v]) => setError(k, v));
            const first = $('.field.has-error', form);
            first && first.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
        }

        setLoading(true);
        try {
            const res = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': $('meta[name="csrf-token"]').content,
                },
                body: JSON.stringify(payload),
            });
            const json = await res.json().catch(() => ({}));

            if (res.ok && json.ok) {
                successText.textContent = json.message || successText.textContent;
                successBox.classList.remove('hidden');
                form.reset();
                successBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
                clearTimeout(successTimer);
                successTimer = setTimeout(() => successBox.classList.add('hidden'), 7000);
            } else {
                if (json.errors) Object.entries(json.errors).forEach(([k, v]) => setError(k, v));
                showToast(json.message || 'Une erreur est survenue. Réessayez.');
            }
        } catch {
            showToast('Connexion impossible. Vérifiez votre réseau et réessayez.');
        } finally {
            setLoading(false);
        }
    });

    // Pré-sélection du lot via /devis?lot=CVC (liens depuis les pages d'expertise)
    const wanted = new URLSearchParams(location.search).getAll('lot');
    wanted.forEach((v) => {
        const box = $(`input[name="lots"][value="${CSS.escape(v)}"]`, form);
        if (box) box.checked = true;
    });
    }

    // ---------- Thème clair / sombre ----------
    const root = document.documentElement;
    const themeBtns = $$('.theme-toggle');
    const metaTheme = $('meta[name="theme-color"]');
    const applyTheme = (light) => {
        root.classList.toggle('light', light);
        themeBtns.forEach((b) => b.setAttribute('aria-pressed', String(light)));
        if (metaTheme) metaTheme.setAttribute('content', light ? '#f4f7fb' : '#070c1a');
    };
    applyTheme(root.classList.contains('light'));
    themeBtns.forEach((b) => b.addEventListener('click', () => {
        const light = !root.classList.contains('light');
        root.classList.add('theme-anim');
        applyTheme(light);
        setTimeout(() => root.classList.remove('theme-anim'), 450);
        try { localStorage.setItem('egc-theme', light ? 'light' : 'dark'); } catch (e) {}
    }));
})();
